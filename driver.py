import sys
from parser import Parser
from traveller import Traveller


def main():
    if len(sys.argv) < 4:
        raise Exception("Cannot provide conflict resolution without giving at least 3 file parameters")

    file_ = {
        'ancestor_path': sys.argv[1],
        'current_path': sys.argv[2],
        'diff_path': sys.argv[3]
    }
    file_['ancestor'] = open(file_['ancestor_path'], 'r').read()
    file_['current'] = open(file_['current_path'], 'r').read()
    file_['diff'] = open(file_['diff_path'], 'r').read()

    traveller = Traveller(
        Parser.parse_code(file_['ancestor']),
        Parser.parse_code(file_['current']),
        Parser.parse_code(file_['diff'])
    )
    result_tree = traveller.travel()

    result_code = Parser.unparse_tree(result_tree)
    # TODO run formatters like yapf?

    with open(file_['current_path'], 'w') as f:
        f.write(result_code)


if __name__ == "__main__":
    main()
