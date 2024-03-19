import argparse
import fileinput
import re
from functools import reduce
from typing import List

RANGE = re.compile(r"(?P<start>\d+)-(?P<stop>\d+)")


def parse_columns(spec: str) -> List[int]:
    values = spec.split(",")
    slices = []
    for value in values:
        if value.isnumeric():
            slices.append(slice(int(value) - 1))
        elif m := RANGE.match(value):
            start = int(m.group("start")) - 1
            stop = int(m.group("stop")) - 1
            if start <= stop:
                slices.append(slice(start, stop + 1))
            else:
                slices.append(slice(start, stop - 1, -1))
        elif "-" in value:
            a, b = value.split("-")
            if a == "":
                slices.append(slice(None, int(b)))
            elif b == "":
                slices.append(slice(int(a) - 1, None))
    return slices


def flatten_list(matrix: List[List]) -> List:
    return list(reduce(lambda x, y: x + y, matrix, []))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "columns",
        type=parse_columns,
        nargs="+",
        help="desired columns",
    )
    parser.add_argument("-w", "--width", type=int, default=3)
    parser.add_argument("-s", "--sep", type=str, default=" ")

    args = parser.parse_args()
    slices = flatten_list(args.columns)

    for line in fileinput.input("-"):
        parts = line.strip().split()

        out = []
        for s in slices:
            for part in parts[s]:
                val = f"{part:>{args.width}}"
                out.append(val)

        print(*out, sep=args.sep, end="")
