from tests.files.helpers import create_conflict_handler


def default_merger_test(merger, path, merger_test_files_path):
    conflict, result_file = create_conflict_handler(path, merger_test_files_path)

    _, result, _ = merger(conflict).merge()

    with open(result_file, 'r') as rfd:
        expected_content = rfd.read()

    if not result.endswith('\n'):
        result = "{}\n".format(result)  # workaround for some tools forgetting about \n at EOF

    assert expected_content == result
