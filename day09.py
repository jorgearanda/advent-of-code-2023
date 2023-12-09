from loader import load_strs


def get_sequences(line):
    cur_seq = [int(x) for x in line.split()]
    seqs = [cur_seq]
    while any(reading != 0 for reading in cur_seq):
        cur_seq = [cur_seq[i] - cur_seq[i - 1] for i in range(1, len(cur_seq))]
        seqs.append(cur_seq)
    return seqs


def predict(line, backwards=False):
    if not backwards:
        return sum(seq[-1] for seq in get_sequences(line))
    prediction = 0
    seqs = get_sequences(line)
    for i in range(len(seqs) - 2, -1, -1):
        prediction = seqs[i][0] - prediction
    return prediction


def sum_predictions(lines, backwards=False):
    return sum(predict(line, backwards) for line in lines)


if __name__ == "__main__":
    lines = load_strs("inputs/day09.txt")
    print(f"Part 1: {sum_predictions(lines)}")
    print(f"Part 2: {sum_predictions(lines, backwards=True)}")


# -- Tests --
fixture = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]


def test_predict():
    assert predict("0 3 6 9 12 15") == 18
    assert predict("1 3 6 10 15 21") == 28
    assert predict("10 13 16 21 30 45") == 68


def test_part_1():
    assert sum_predictions(fixture) == 114


def test_predict_backwards():
    assert predict("0 3 6 9 12 15", backwards=True) == -3
    assert predict("1 3 6 10 15 21", backwards=True) == 0
    assert predict("10 13 16 21 30 45", backwards=True) == 5


def test_part_2():
    assert sum_predictions(fixture, backwards=True) == 2
