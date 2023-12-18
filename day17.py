from heapq import heappop, heappush

from loader import load_strs


def shortest_path(nodes):
    visited = set()
    queue = []
    heappush(queue, (0, 0, 0, 0, 0, 0))

    while queue:
        cost, row, col, dir_row, dir_col, steps_straight = heappop(queue)
        if row == len(nodes) - 1 and col == len(nodes[0]) - 1:
            return cost

        if (row, col, dir_row, dir_col, steps_straight) in visited:
            continue
        visited.add((row, col, dir_row, dir_col, steps_straight))

        if steps_straight < 3 and (dir_row, dir_col) != (0, 0):
            next_row = row + dir_row
            next_col = col + dir_col
            if 0 <= next_row < len(nodes) and 0 <= next_col < len(nodes[0]):
                heappush(
                    queue,
                    (
                        cost + nodes[next_row][next_col],
                        next_row,
                        next_col,
                        dir_row,
                        dir_col,
                        steps_straight + 1,
                    ),
                )
        for next_dir_row, next_dir_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (next_dir_row, next_dir_col) in [
                (dir_row, dir_col),
                (-dir_row, -dir_col),
            ]:
                continue
            next_row = row + next_dir_row
            next_col = col + next_dir_col
            if 0 <= next_row < len(nodes) and 0 <= next_col < len(nodes[0]):
                heappush(
                    queue,
                    (
                        cost + nodes[next_row][next_col],
                        next_row,
                        next_col,
                        next_dir_row,
                        next_dir_col,
                        1,
                    ),
                )


def shortest_path_ultra(nodes):
    visited = set()
    queue = []
    heappush(queue, (0, 0, 0, 0, 1, 0))
    heappush(queue, (0, 0, 0, 1, 0, 0))

    while queue:
        cost, row, col, dir_row, dir_col, steps_straight = heappop(queue)
        if row == len(nodes) - 1 and col == len(nodes[0]) - 1:
            return cost

        if (row, col, dir_row, dir_col, steps_straight) in visited:
            continue
        visited.add((row, col, dir_row, dir_col, steps_straight))

        if steps_straight < 10 and (dir_row, dir_col) != (0, 0):
            next_row = row + dir_row
            next_col = col + dir_col
            if 0 <= next_row < len(nodes) and 0 <= next_col < len(nodes[0]):
                heappush(
                    queue,
                    (
                        cost + nodes[next_row][next_col],
                        next_row,
                        next_col,
                        dir_row,
                        dir_col,
                        steps_straight + 1,
                    ),
                )
        if steps_straight < 4:
            continue
        for next_dir_row, next_dir_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (next_dir_row, next_dir_col) in [
                (dir_row, dir_col),
                (-dir_row, -dir_col),
            ]:
                continue
            next_row = row + next_dir_row
            next_col = col + next_dir_col
            if 0 <= next_row < len(nodes) and 0 <= next_col < len(nodes[0]):
                heappush(
                    queue,
                    (
                        cost + nodes[next_row][next_col],
                        next_row,
                        next_col,
                        next_dir_row,
                        next_dir_col,
                        1,
                    ),
                )


def get_nodes(lines):
    return [[int(node) for node in line] for line in lines]


if __name__ == "__main__":
    nodes = get_nodes(load_strs("inputs/day17.txt"))
    print(f"Part 1: {shortest_path(nodes)}")
    print(f"Part 2: {shortest_path_ultra(nodes)}")


# -- Tests --
fixture = [
    "2413432311323",
    "3215453535623",
    "3255245654254",
    "3446585845452",
    "4546657867536",
    "1438598798454",
    "4457876987766",
    "3637877979653",
    "4654967986887",
    "4564679986453",
    "1224686865563",
    "2546548887735",
    "4322674655533",
]


def test_get_nodes():
    nodes = get_nodes(fixture)
    assert len(nodes) == 13
    assert len(nodes[0]) == 13
    assert nodes[0][0] == 2


def test_shortest_path():
    nodes = get_nodes(fixture)
    assert shortest_path(nodes) == 102


def test_shortest_path_ultra():
    nodes = get_nodes(fixture)
    assert shortest_path_ultra(nodes) == 94
