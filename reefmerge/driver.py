from argparse import ArgumentParser

from reefmerge.conflict_handler import ConflictHandler
from reefmerge.merger import Merger


def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if len(args.files) < 3:
        raise Exception("Cannot work with less than 3 arguments")
    # TODO check if files exists?

    conflict_handler = ConflictHandler(
        ancestor_filepath=args.files[0],
        mine_filepath=args.files[1],
        yours_filepath=args.files[2]
    )

    merger = Merger(conflict_handler=conflict_handler)
    merger.merge(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
