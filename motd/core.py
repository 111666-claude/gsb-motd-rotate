"""轮播选取核心。"""


class Counter:
    """记录本轮检查过的公告条数。"""

    def __init__(self):
        self.scanned = 0


def _in_window(entry, tick):
    return entry["start"] <= tick < entry["end"]


def new_rotation(announcements):
    ordered = sorted(announcements, key=lambda entry: entry["id"])
    ring = []
    for entry in ordered:
        ring.extend([entry] * int(entry.get("weight", 1)))
    pinned = [entry for entry in ordered if entry.get("pinned")]
    return {
        "ring": ring,
        "pinned": pinned,
        "cursor": 0,
        "last": None,
    }


def pick(rotation, tick, counter):
    last = rotation["last"]
    if last is not None and last[0] == tick:
        replay = dict(last[1])
        replay["status"] = "replay"
        return replay

    chosen = None
    for entry in rotation["pinned"]:
        counter.scanned += 1
        if _in_window(entry, tick):
            chosen = entry["id"]
            break

    if chosen is None:
        ring = rotation["ring"]
        attempts = 0
        while ring and attempts < len(ring):
            entry = ring[rotation["cursor"] % len(ring)]
            rotation["cursor"] += 1
            counter.scanned += 1
            attempts += 1
            if _in_window(entry, tick):
                chosen = entry["id"]
                break

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
