from loader import load_strs

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def first_digit(s, spelled=False):
    for i in range(len(s)):
        if s[i].isdigit():
            return int(s[i])
        if spelled:
            for key in digits:
                if s[i:].startswith(key):
                    return digits[key]


def last_digit(s, spelled=False):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isdigit():
            return int(s[i])
        if spelled:
            for key in digits:
                if s[: i + 1].endswith(key):
                    return digits[key]


def calibration(s):
    return first_digit(s) * 10 + last_digit(s)


def calibration_spelled(s):
    return first_digit(s, spelled=True) * 10 + last_digit(s, spelled=True)


def calibration_sum(lines):
    return sum(calibration(line) for line in lines)


def calibration_sum_spelled(lines):
    return sum(calibration_spelled(line) for line in lines)


if __name__ == "__main__":
    lines = load_strs("inputs/day01.txt")

    print(f"Part 1: {calibration_sum(lines)}")
    print(f"Part 2: {calibration_sum_spelled(lines)}")


# -- Tests --
fixture = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]
fixture2 = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]


def test_calibration():
    assert calibration("1abc2") == 12
    assert calibration("treb7uchet") == 77


def test_part_1():
    assert calibration_sum(fixture) == 142


def test_calibration_spelled():
    assert calibration_spelled("two1nine") == 29


def test_part_2():
    assert calibration_sum_spelled(fixture2) == 281
