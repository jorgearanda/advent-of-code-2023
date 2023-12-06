from loader import load_strs


class MapRange:
    def __init__(self, dst_start, src_start, span):
        self.dst_start = int(dst_start)
        self.dst_end = int(dst_start) + int(span)
        self.src_start = int(src_start)
        self.src_end = int(src_start) + int(span)
        self.diff = self.dst_start - self.src_start

    def __lt__(self, other):
        return self.src_start < other.src_start


class Almanac:
    def __init__(self, lines, seeds_are_ranges=False):
        self.set_seed_ranges(lines, seeds_are_ranges)
        self.set_maps_and_destinations(lines)

    def set_seed_ranges(self, lines, seeds_are_ranges):
        seed_tokens = [int(category) for category in lines[0][7:].split()]
        if seeds_are_ranges:
            self.seed_ranges = sorted(
                [
                    [seed_tokens[i], seed_tokens[i] + seed_tokens[i + 1]]
                    for i in range(0, len(seed_tokens), 2)
                ]
            )
        else:
            self.seed_ranges = sorted(
                [seed_tokens[i], seed_tokens[i] + 1] for i in range(len(seed_tokens))
            )

    def set_maps_and_destinations(self, lines):
        self.destinations = {}
        self.maps = {}
        for line in lines[2:]:
            if len(line) == 0:
                continue
            if "map" in line:
                src, dst = line.split()[0].split("-to-")
                self.destinations[src] = dst
                self.maps[src] = []
                continue
            dst_start, src_start, span = line.split()
            self.maps[src].append(MapRange(dst_start, src_start, span))
        for key in self.maps:
            self.maps[key] = sorted(self.maps[key])

    def resolve_for(self, src, spans):
        next_spans = []
        cur_span_idx = 0
        cur_span = spans[cur_span_idx]
        cur_map_idx = 0
        cur_map = self.maps[src][cur_map_idx]
        while True:
            if cur_span[0] < cur_map.src_start:
                # At least part of the current span is not mapped, so goes through
                if cur_span[1] <= cur_map.src_start:
                    # The whole current span is not mapped and can be passed through
                    next_spans.append(cur_span)
                    if len(spans) <= cur_span_idx + 1:
                        break
                    cur_span_idx += 1
                    cur_span = spans[cur_span_idx]
                else:
                    # Break it off into an unmapped and a next piece
                    next_spans.append([cur_span[0], cur_map.src_start])
                    cur_span = [cur_map.src_start, cur_span[1]]
                continue
            elif cur_map.src_end <= cur_span[0]:
                # The current map is behind the current span
                if len(self.maps[src]) <= cur_map_idx + 1:
                    # There are no more maps, pass through the rest of the current span
                    next_spans.append(cur_span)
                    if len(spans) <= cur_span_idx + 1:
                        break
                    cur_span_idx += 1
                    cur_span = spans[cur_span_idx]
                else:
                    # Shift current map, will try again
                    cur_map_idx += 1
                    cur_map = self.maps[src][cur_map_idx]
                continue
            else:
                # The current span starts within the current map
                if cur_span[1] <= cur_map.src_end:
                    # Fully enclosed, map it and shift
                    next_spans.append(
                        [cur_span[0] + cur_map.diff, cur_span[1] + cur_map.diff]
                    )
                    if len(spans) <= cur_span_idx + 1:
                        break
                    cur_span_idx += 1
                    cur_span = spans[cur_span_idx]
                else:
                    # Map the piece that is enclosed, will try again with the rest
                    next_spans.append([cur_span[0] + cur_map.diff, cur_map.dst_end])
                    cur_span = [cur_map.src_end, cur_span[1]]

        return sorted(next_spans)

    def lowest_location(self):
        src = "seed"
        spans = self.seed_ranges
        while src in self.destinations:
            spans = self.resolve_for(src, spans)
            src = self.destinations[src]
        return min(spans)[0]


if __name__ == "__main__":
    almanac = Almanac(load_strs("inputs/day05.txt"))
    print(f"Part 1: {almanac.lowest_location()}")
    almanac = Almanac(load_strs("inputs/day05.txt"), seeds_are_ranges=True)
    print(f"Part 2: {almanac.lowest_location()}")


# -- Tests --
fixture = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


def test_part_1():
    almanac = Almanac(fixture)
    assert almanac.lowest_location() == 35


def test_seed_ranges():
    almanac = Almanac(fixture, seeds_are_ranges=True)
    assert almanac.seed_ranges == [[55, 68], [79, 93]]


def test_maps_and_destinations():
    almanac = Almanac(fixture, seeds_are_ranges=True)
    assert almanac.maps["fertilizer"][0].src_start == 0  # sorted by src_start
    assert almanac.maps["fertilizer"][1].src_start == 7
    assert almanac.maps["fertilizer"][2].src_start == 11
    assert almanac.maps["fertilizer"][3].src_start == 53
    assert almanac.destinations["fertilizer"] == "water"


def test_resolve_for():
    almanac = Almanac(fixture, seeds_are_ranges=True)
    soil_ranges = almanac.resolve_for("seed", almanac.seed_ranges)
    assert soil_ranges == [[57, 70], [81, 95]]
    fertilizer_ranges = almanac.resolve_for("soil", soil_ranges)
    assert fertilizer_ranges == [[57, 70], [81, 95]]


def test_part_2():
    almanac = Almanac(fixture, seeds_are_ranges=True)
    assert almanac.lowest_location() == 46
