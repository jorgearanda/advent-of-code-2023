from math import prod

from loader import load_strs


class Game:
    def __init__(self, record):
        label, turns_str = record.split(": ")
        self.id = int(label.split()[1])
        self.turns = [Turn(turn_str) for turn_str in turns_str.split("; ")]
        self.fewest = {}
        for turn in self.turns:
            for key in turn.cubes.keys():
                self.fewest[key] = max(self.fewest.get(key, 0), turn.cubes[key])
        self.valid = all(turn.valid for turn in self.turns)
        self.power = prod(self.fewest.values())


class Turn:
    def __init__(self, turn_record):
        self.cubes = {}
        for subset in turn_record.split(", "):
            qty, colour = subset.split()
            self.cubes[colour] = int(qty)
        self.valid = (
            self.cubes.get("red", 0) <= 12
            and self.cubes.get("green", 0) <= 13
            and self.cubes.get("blue", 0) <= 14
        )


def valid_games_sum(games):
    return sum(game.id for game in games if game.valid)


def game_power_sum(games):
    return sum(game.power for game in games)


if __name__ == "__main__":
    games = [Game(record) for record in load_strs("inputs/day02.txt")]
    print(f"Part 1: {valid_games_sum(games)}")
    print(f"Part 2: {game_power_sum(games)}")


# -- Tests --
fixture = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


def test_turn():
    assert Turn("3 blue, 4 red").valid
    assert not Turn("8 green, 6 blue, 20 red").valid


def test_game():
    assert Game(fixture[1]).valid
    assert not Game(fixture[3]).valid


def test_part_1():
    games = [Game(record) for record in fixture]
    assert valid_games_sum(games) == 8


def test_power():
    assert Game(fixture[0]).power == 48


def test_part_2():
    games = [Game(record) for record in fixture]
    assert game_power_sum(games) == 2286
