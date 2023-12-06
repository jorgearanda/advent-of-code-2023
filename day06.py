import math

from loader import load_strs


def solve(time, distance):
    """
    If distance = speed * time_moving,
    speed = time_accelerating,
    and time = time_accelerating + time_moving,
    then -time_accelerating**2 + time * time_accelerating - distance = 0.
    """
    sol1 = math.ceil((-time + math.sqrt(time**2 - 4 * distance)) / -2)
    if sol1 * (time - sol1) == distance:
        # Some solutions meet, but do not exceed, the record
        sol1 += 1

    sol2 = math.floor((-time - math.sqrt(time**2 - 4 * distance)) / -2)
    if sol2 * (time - sol2) == distance:
        sol2 -= 1

    return (sol1, sol2)


def ways_to_win(time, distance):
    sol1, sol2 = solve(time, distance)
    return sol2 - sol1 + 1


def parse(lines):
    times = lines[0].split()[1:]
    distances = lines[1].split()[1:]
    return [
        {"time": int(time), "distance": int(distance)}
        for time, distance in zip(times, distances)
    ]


def parse_as_one_race(lines):
    return [
        {
            "time": int(lines[0][11:].replace(" ", "")),
            "distance": int(lines[1][11:].replace(" ", "")),
        }
    ]


def ways_to_win_product(lines, one_race=False):
    races = parse_as_one_race(lines) if one_race else parse(lines)
    return math.prod(ways_to_win(race["time"], race["distance"]) for race in races)


if __name__ == "__main__":
    lines = load_strs("inputs/day06.txt")
    print(f"Part 1: {ways_to_win_product(lines)}")
    print(f"Part 2: {ways_to_win_product(lines, one_race=True)}")


# -- Tests --
fixture = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


def test_solve():
    assert solve(7, 9) == (2, 5)
    assert solve(15, 40) == (4, 11)
    assert solve(30, 200) == (11, 19)


def test_part_1():
    assert ways_to_win_product(fixture) == 288


def test_part_2():
    assert ways_to_win_product(fixture, one_race=True) == 71503
