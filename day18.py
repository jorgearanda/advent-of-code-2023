from loader import load_strs


def get_instruction(line, hexed=False):
    if hexed:
        hex_instruction = line.split()[-1][2:-1]
        direction = ""
        match hex_instruction[-1]:
            case "0":
                direction = "R"
            case "1":
                direction = "D"
            case "2":
                direction = "L"
            case "3":
                direction = "U"
        return (direction, int(hex_instruction[:-1], 16))
    else:
        direction, amount, _ = line.split()
        return (direction, amount)


def shoelace(instructions, hexed=False):
    res = 0
    x = y = prev_x = prev_y = 0
    border = 0
    for line in instructions:
        direction, amount = get_instruction(line, hexed)
        amount = int(amount)
        border += amount
        match direction:
            case "U":
                y += amount
            case "D":
                y -= amount
            case "R":
                x += amount
            case "L":
                x -= amount
        res += prev_x * y - prev_y * x
        prev_x = x
        prev_y = y
    return int((abs(res) + border) / 2 + 1)


if __name__ == "__main__":
    instructions = load_strs("inputs/day18.txt")
    print(f"Part 1: {shoelace(instructions)}")
    print(f"Part 2: {shoelace(instructions, hexed=True)}")


# -- Tests --
square = [
    "R 5 top",
    "D 5 side",
    "L 5 bottom",
    "U 5 side",
]

fixture = [
    "R 6 (#70c710)",
    "D 5 (#0dc571)",
    "L 2 (#5713f0)",
    "D 2 (#d2c081)",
    "R 2 (#59c680)",
    "D 2 (#411b91)",
    "L 5 (#8ceee2)",
    "U 2 (#caa173)",
    "L 1 (#1b58a2)",
    "U 2 (#caa171)",
    "R 2 (#7807d2)",
    "U 3 (#a77fa3)",
    "L 2 (#015232)",
    "U 2 (#7a21e3)",
]


def test_shoelace_square():
    assert shoelace(square) == 36


def test_shoelace():
    assert shoelace(fixture) == 62


def test_shoelace_hexed():
    assert shoelace(fixture, hexed=True) == 952408144115
