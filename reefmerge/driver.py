import sys

from reefmerge.constants import Version
from reefmerge.merger import Merger


def main():
    if len(sys.argv) < 4:
        raise Exception("Cannot work with less than 3 arguments")
    # TODO check if files exists?

    files = {
        Version.ANCESTOR: sys.argv[1],
        Version.MINE: sys.argv[2],
        Version.YOURS: sys.argv[3],
    }

    merger = Merger(files=files)
    merger.merge()


if __name__ == "__main__":
    main()
