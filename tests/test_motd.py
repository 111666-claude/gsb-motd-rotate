import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motd import core


def ann(aid, weight=1, start=0, end=10 ** 9, pinned=False):
    return {"id": aid, "weight": weight, "start": start, "end": end, "pinned": pinned}


class MotdTest(unittest.TestCase):
    def test_single_announcement_is_picked(self):
        out = core.pick(core.new_rotation([ann("a")]), 0, core.Counter())
        self.assertEqual(out["id"], "a")
        self.assertEqual(out["status"], "ok")

    def test_no_announcement_gives_null(self):
        out = core.pick(core.new_rotation([]), 0, core.Counter())
        self.assertIsNone(out["id"])

    def test_rotation_advances_in_id_order(self):
        picked = core.run([ann("a"), ann("b")], 2, 0, 1000)
        self.assertEqual([p["id"] for p in picked], ["a", "b"])

    def test_each_tick_reports_its_time(self):
        picked = core.run([ann("a")], 3, 100, 50)
        self.assertEqual([p["tick"] for p in picked], [100, 150, 200])

    def test_run_returns_one_line_per_tick(self):
        self.assertEqual(len(core.run([ann("a")], 4, 0, 10)), 4)


if __name__ == "__main__":
    unittest.main()
