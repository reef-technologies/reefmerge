import sys

from reefmerge.files_handler import Files
from reefmerge.merger import Merger


def main():
    if len(sys.argv) < 4:
        raise Exception("Cannot work with less than 3 arguments")
    # TODO check if files exists?

    files = Files(
        ancestor=sys.argv[1],
        mine=sys.argv[2],
        yours=sys.argv[3]
    )
    dry_run = "-d" in sys.argv

    merger = Merger(files=files)
    merger.merge(dry_run=dry_run)


if __name__ == "__main__":
    main()
