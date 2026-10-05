"""命令行入口。"""

import argparse
import json

from . import core


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="motd")
    ap.add_argument("--sample", choices=["window", "pin", "weight", "replay", "work"])
    sub = ap.add_subparsers(dest="cmd")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--announcements", required=True)
    run_parser.add_argument("--ticks", type=int, default=1)
    run_parser.add_argument("--start", type=int, default=0)
    run_parser.add_argument("--step", type=int, default=30000)
    args = ap.parse_args(argv)

    if args.sample:
        from . import samples
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    for out in core.run(_load(args.announcements), args.ticks, args.start, args.step):
        print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
