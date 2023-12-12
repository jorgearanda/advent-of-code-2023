from functools import cache

from loader import load_strs


@cache
def valid_arrangements(springs, clusters):
    if len(clusters) == 0:
        return 1 if "#" not in springs else 0
    if len(springs) == 0:  # but we still have clusters
        return 0
    res = 0
    if springs[0] in ".?":
        res += valid_arrangements(springs[1:], clusters)
    if (
        springs[0] in "#?"
        and clusters[0] <= len(springs)
        and "." not in springs[: clusters[0]]
        and (clusters[0] == len(springs) or springs[clusters[0]] != "#")
    ):
        res += valid_arrangements(springs[clusters[0] + 1 :], clusters[1:])
    return res


def sum_arrangements(springs, unfold=False):
    res = 0
    for spring in springs:
        line, cluster_strs = spring.split()
        clusters = tuple(int(cluster) for cluster in cluster_strs.split(","))
        if unfold:
            line = "?".join([line] * 5)
            clusters *= 5
        res += valid_arrangements(line, clusters)
    return res


if __name__ == "__main__":
    springs = load_strs("inputs/day12.txt")
    print(f"Part 1: {sum_arrangements(springs)}")
    print(f"Part 2: {sum_arrangements(springs, unfold=True)}")


# -- Tests --
fixture = [
    "???.### 1,1,3",
    ".??..??...?##. 1,1,3",
    "?#?#?#?#?#?#?#? 1,3,1,6",
    "????.#...#... 4,1,1",
    "????.######..#####. 1,6,5",
    "?###???????? 3,2,1",
]


def test_arrangements():
    assert valid_arrangements("???.###", (1, 1, 3)) == 1
    assert valid_arrangements(".??..??...?##.", (1, 1, 3)) == 4
    assert valid_arrangements("?###????????", (3, 2, 1)) == 10


def test_part_1():
    assert sum_arrangements(fixture) == 21


def test_part_2():
    assert sum_arrangements(fixture, unfold=True) == 525152
