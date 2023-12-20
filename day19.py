from copy import deepcopy
from math import prod

from loader import load_strs


def parse_rule(line):
    name = line[: line.index("{")]
    steps = line[line.index("{") + 1 : line.index("}")].split(",")
    parsed_steps = []
    for step in steps:
        if ":" in step:
            parsed_steps.append(
                {
                    "cat": step[0],
                    "sign": step[1],
                    "val": int(step[2 : step.index(":")]),
                    "outcome": step[step.index(":") + 1 :],
                }
            )
        else:
            parsed_steps.append({"outcome": step})
    return name, parsed_steps


def parse_part(line):
    cats = line[1:-1].split(",")
    return {cat[0]: int(cat[2:]) for cat in cats}


def parse_system(lines):
    rules = {}
    parts = []
    doing_rules = True
    for line in lines:
        if line == "":
            doing_rules = False
            continue
        if doing_rules:
            name, steps = parse_rule(line)
            rules[name] = steps
        else:
            parts.append(parse_part(line))
    return rules, parts


def workflow(part, rules):
    on_workflow = "in"
    while True:
        if on_workflow not in rules:
            return on_workflow
        for step in rules[on_workflow]:
            if "cat" not in step:
                on_workflow = step["outcome"]
                break
            if step["sign"] == "<":
                if part[step["cat"]] < step["val"]:
                    on_workflow = step["outcome"]
                    break
            elif part[step["cat"]] > step["val"]:
                on_workflow = step["outcome"]
                break


def process(lines):
    rules, parts = parse_system(lines)
    accepted = [part for part in parts if workflow(part, rules) == "A"]
    return sum(sum(part.values()) for part in accepted)


def valid_spans(lines):
    rules, _ = parse_system(lines)
    spans = {"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)}
    return accepted_parts(rules, "in", 0, spans)


def accepted_parts(rules, name, step, spans):
    if name == "R":
        return 0
    if name == "A":
        return prod(spans[key][1] - spans[key][0] for key in spans)
    if "cat" not in rules[name][step]:
        if rules[name][step]["outcome"] == "R":
            return 0
        elif rules[name][step]["outcome"] == "A":
            return prod(spans[key][1] - spans[key][0] for key in spans)
        else:
            return accepted_parts(rules, rules[name][step]["outcome"], 0, spans)
    else:
        if rules[name][step]["sign"] == "<":
            true_span = (
                spans[rules[name][step]["cat"]][0],
                min(spans[rules[name][step]["cat"]][1], rules[name][step]["val"]),
            )
            false_span = (
                min(spans[rules[name][step]["cat"]][1], rules[name][step]["val"]),
                spans[rules[name][step]["cat"]][1],
            )
        else:
            true_span = (
                max(spans[rules[name][step]["cat"]][0], rules[name][step]["val"] + 1),
                spans[rules[name][step]["cat"]][1],
            )
            false_span = (
                spans[rules[name][step]["cat"]][0],
                max(spans[rules[name][step]["cat"]][0], rules[name][step]["val"] + 1),
            )
        spans = deepcopy(spans)
        spans[rules[name][step]["cat"]] = true_span
        accepted = accepted_parts(rules, rules[name][step]["outcome"], 0, spans)
        if len(rules[name]) > step + 1:
            spans = deepcopy(spans)
            spans[rules[name][step]["cat"]] = false_span
            accepted += accepted_parts(rules, name, step + 1, spans)
        return accepted


if __name__ == "__main__":
    lines = load_strs("inputs/day19.txt")
    print(f"Part 1: {process(lines)}")
    print(f"Part 2: {valid_spans(lines)}")

# -- Tests --
fixture = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
    "",
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]


def test_parse():
    rules, parts = parse_system(fixture)
    assert len(rules) == 11
    assert len(parts) == 5
    assert len(rules["px"]) == 3
    assert rules["px"][0]["cat"] == "a"
    assert rules["px"][0]["sign"] == "<"
    assert rules["px"][0]["val"] == 2006
    assert rules["px"][0]["outcome"] == "qkq"
    assert parts[-1]["m"] == 1623


def test_workflow():
    rules, parts = parse_system(fixture)
    assert workflow(parts[0], rules) == "A"
    assert workflow(parts[1], rules) == "R"


def test_part_1():
    assert process(fixture) == 19114


def test_part_2():
    assert valid_spans(fixture) == 167409079868000
