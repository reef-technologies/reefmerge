from argparse import ArgumentParser

from reefmerge.conflict import Conflict
from reefmerge.merger_sequence import MergerSequence

from reefmerge.resolvers.isort import ISortMerger
from reefmerge.resolvers.yapf import YapfMerger


def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if len(args.files) < 3:
        raise Exception("Cannot work with less than 3 arguments")
    # TODO check if files exists?

    conflict = Conflict.from_paths(
        ancestor_filepath=args.files[0],
        mine_filepath=args.files[1],
        yours_filepath=args.files[2]
    )

    merger = MergerSequence(conflict=conflict, mergers_list=[ISortMerger, YapfMerger])
    merger.merge(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
