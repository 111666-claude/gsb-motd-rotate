"""轮播选取核心。"""


class Counter:
    """记录本轮检查过的公告条数。"""

    def __init__(self):
        self.scanned = 0


def new_rotation(announcements):
    return {"announcements": list(announcements), "cursor": 0, "last": None}


def pick(rotation, tick, counter):
    cycle = []
    for entry in rotation["announcements"]:
        counter.scanned += 1
        cycle.append(entry["id"])
    if not cycle:
        rotation["last"] = (tick, None)
        return {"tick": tick, "id": None, "status": "ok", "scanned": counter.scanned}
    chosen = cycle[rotation["cursor"] % len(cycle)]
    rotation["cursor"] += 1
    rotation["last"] = (tick, chosen)
    return {"tick": tick, "id": chosen, "status": "ok", "scanned": counter.scanned}


def run(announcements, ticks, start, step, counter=None):
    counter = counter or Counter()
    rotation = new_rotation(announcements)
    out = []
    for i in range(ticks):
        out.append(pick(rotation, start + i * step, counter))
    return out
