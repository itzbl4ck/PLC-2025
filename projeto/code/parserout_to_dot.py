import re

states = set()
edges = []

current_state = None

with open("parser.out", encoding="utf-8") as f:
    for line in f:
        # state X
        m = re.match(r"state (\d+)", line)
        if m:
            current_state = m.group(1)
            states.add(current_state)
            continue

        # shift / goto
        m = re.search(r"(\S+)\s+(shift and go to state|go to state)\s+(\d+)", line)
        if m and current_state is not None:
            symbol, _, target = m.groups()
            edges.append((current_state, target, symbol))
            states.add(target)

with open("lr_automaton.dot", "w", encoding="utf-8") as f:
    f.write("digraph LR {\n")
    f.write("  rankdir=LR;\n")
    f.write("  node [shape=circle, fontsize=10];\n")
    f.write("  edge [fontsize=8];\n\n")

    for s in sorted(states, key=int):
        f.write(f'  {s} [label="I{s}"];\n')

    f.write("\n")

    for src, dst, label in edges:
        f.write(f'  {src} -> {dst} [label="{label}"];\n')

    f.write("}\n")
