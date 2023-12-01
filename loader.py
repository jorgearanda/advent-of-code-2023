def load_ints(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def load_comma_ints(filename):
    with open(filename) as f:
        return [int(token) for token in f.read().split(",")]


def load_strs(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f.readlines()]


def load_int_chunks(filename):
    """
    Integers, one per line, separated in chunks by extra newlines.

    Each chunk is returned as a list item within the larger chunks list.
    """
    chunks = []
    lines = load_strs(filename)
    chunk = []
    for line in lines:
        if line == "":
            chunks.append(chunk)
            chunk = []
        else:
            chunk.append(int(line))

    if len(chunk) > 0:
        chunks.append(chunk)

    return chunks


# -- Tests --
def test_load_ints():
    ints = load_ints("fixtures/ints.txt")
    assert ints == [123, 456, 789]


def test_load_comma_ints():
    ints = load_comma_ints("fixtures/comma_ints.txt")
    assert ints == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_load_strs():
    strs = load_strs("fixtures/strs.txt")
    assert strs == ["abc", "def", "ghi"]  # No newline


def test_load_int_chunks():
    int_chunks = load_int_chunks("fixtures/int_chunks.txt")
    assert int_chunks == [[123, 456], [789]]
