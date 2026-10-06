"""轮播选取核心。"""


class Counter:
    """记录本轮检查过的公告条数。"""

    def __init__(self):
        self.scanned = 0


def new_rotation(announcements):
    # 按 id 升序排序，保证轮转环与置顶覆盖层的拼接顺序稳定。
    anns = sorted(announcements, key=lambda a: a["id"])
    events = []
    for idx, entry in enumerate(anns):
        events.append((entry["start"], 0, idx))
        events.append((entry["end"], 1, idx))
    events.sort()
    return {
        "announcements": anns,
        "events": events,
        "next_event": 0,
        "active": [False] * len(anns),
        "ring": None,
        "pinned": None,
        "cursor": 0,
        "last": None,
    }


def _advance_events(rotation, tick, counter):
    # 结算所有时刻不晚于 tick 的 start/end 事件，增量维护活跃集。
    events = rotation["events"]
    active = rotation["active"]
    pos = rotation["next_event"]
    changed = False
    while pos < len(events) and events[pos][0] <= tick:
        _, kind, idx = events[pos]
        active[idx] = kind == 0
        counter.scanned += 1
        changed = True
        pos += 1
    rotation["next_event"] = pos
    if changed:
        rotation["ring"] = None
        rotation["pinned"] = None


def _rebuild(rotation, counter):
    # 活跃集变化后重建轮转环与置顶列表，其余 tick 直接复用。
    ring = []
    pinned = []
    for idx, entry in enumerate(rotation["announcements"]):
        if not rotation["active"][idx]:
            continue
        counter.scanned += 1
        if entry["pinned"]:
            pinned.append(entry["id"])
        else:
            ring.extend([entry["id"]] * entry["weight"])
    rotation["ring"] = ring
    rotation["pinned"] = pinned


def pick(rotation, tick, counter):
    last = rotation["last"]
    if last is not None and last[0] == tick:
        # 同一个 tick 只结算一次，重复请求回放首次结果。
        replay = dict(last[1])
        replay["status"] = "replay"
        return replay

    _advance_events(rotation, tick, counter)
    if rotation["ring"] is None:
        _rebuild(rotation, counter)

    if rotation["pinned"]:
        # 置顶覆盖层优先，且不消耗轮转位。
        chosen = rotation["pinned"][0]
    elif rotation["ring"]:
        chosen = rotation["ring"][rotation["cursor"] % len(rotation["ring"])]
        rotation["cursor"] += 1
    else:
        chosen = None

    result = {"tick": tick, "id": chosen, "status": "ok", "scanned": counter.scanned}
    rotation["last"] = (tick, result)
    return result


def run(announcements, ticks, start, step, counter=None):
    counter = counter or Counter()
    rotation = new_rotation(announcements)
    out = []
    for i in range(ticks):
        out.append(pick(rotation, start + i * step, counter))
    return out
