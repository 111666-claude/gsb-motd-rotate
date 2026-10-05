"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _ann(aid, weight=1, start=0, end=10 ** 9, pinned=False):
    return {"id": aid, "weight": weight, "start": start, "end": end, "pinned": pinned}


def run(name):
    if name == "window":
        anns = [_ann("a", end=1000), _ann("b")]
        out = core.pick(core.new_rotation(anns), 5000, core.Counter())
        _line({"tick": out["tick"], "id": out["id"]})
        return 0
    if name == "pin":
        anns = [_ann("a"), _ann("p", pinned=True)]
        out = core.pick(core.new_rotation(anns), 1000, core.Counter())
        _line({"tick": out["tick"], "id": out["id"]})
        return 0
    if name == "weight":
        anns = [_ann("a", weight=3), _ann("b", weight=1)]
        picked = core.run(anns, 4, 1000, 1000)
        _line({"picked": [p["id"] for p in picked]})
        return 0
    if name == "replay":
        rotation = core.new_rotation([_ann("a"), _ann("b")])
        first = core.pick(rotation, 1000, core.Counter())
        second = core.pick(rotation, 1000, core.Counter())
        _line({"call": 1, "status": first["status"], "id": first["id"]})
        _line({"call": 2, "status": second["status"], "id": second["id"]})
        return 0
    if name == "work":
        anns = [_ann("a%03d" % i) for i in range(40)]
        counter = core.Counter()
        core.run(anns, 3000, 0, 1000, counter)
        _line({"ticks": 3000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
