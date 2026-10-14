"""0/1 Knapsack (Dynamic Programming) with an ASCII visualization of the DP table.

Works in a normal terminal AND in online compilers (Programiz, OnlineGDB, Replit...):
  * If "Knapsack data (2).txt" is not found, the built-in copy of the test data is used.
  * Real terminal  -> live animation, one frame per cell.
  * Online compiler / output piped -> prints the table after each item row (no screen clearing).
  * Writing result.txt is optional; failure to write does not crash the program.

Usage:
    python knapsack.py                 # auto mode
    python knapsack.py data.txt        # use another data file
    python knapsack.py --fast          # results only, no table
"""
import sys
import time

INPUT = "Knapsack data (2).txt"
OUTPUT = "result.txt"

EMBEDDED = """#Test
4 10
5 60
3 50
4 70
2 30
#Test
5 15
2 10
3 20
4 30
5 40
9 50
#Test
6 12
1 10
2 15
3 40
8 90
4 50
5 60
#Test
5 8
3 30
4 50
2 20
1 10
5 60
#Test
7 20
2 12
3 18
4 25
5 35
9 50
7 40
6 30
#Test
4 6
1 20
2 30
3 40
4 50
#Test
5 25
12 24
7 13
11 23
8 15
9 16
#Test
6 18
3 10
5 20
6 30
2 15
4 25
7 35
#Test
8 30
4 10
8 40
5 30
3 50
6 70
2 20
9 60
7 80
#Test
10 50
5 10
10 20
15 30
22 40
25 50
30 60
35 70
40 80
45 90
50 100
"""


def parse_text(text):
    """Split on lines starting with '#Test'; first line 'n W', then n 'weight value' lines."""
    blocks, block = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#Test"):
            if block:
                blocks.append(block)
            block = []
        elif line and block is not None:
            block.append(tuple(map(int, line.split())))
    if block:
        blocks.append(block)
    cases = []
    for b in blocks:
        n, W = b[0]
        cases.append((n, W, b[1:1 + n]))
    return cases


def load_cases(path):
    try:
        with open(path) as f:
            return parse_text(f.read()), path
    except (OSError, UnicodeDecodeError):
        return parse_text(EMBEDDED), "built-in data (file not found)"


def render(dp, items, W, cur_i, cur_w, note, clear):
    """Draw the DP table; the cell being computed is shown as [v]."""
    n = len(items)
    out = []
    if clear:
        out.append("\033[H\033[J")
    out.append(note)
    out.append("")
    head = "item (w,v) | " + " ".join(f"{c:>4}" for c in range(W + 1))
    out.append(head)
    out.append("-" * len(head))
    for i in range(n + 1):
        label = "none       " if i == 0 else f"#{i} ({items[i-1][0]},{items[i-1][1]})".ljust(11)
        cells = []
        for c in range(W + 1):
            v = dp[i][c]
            if i == cur_i and c == cur_w:
                cells.append(f"[{v}]".rjust(4))
            elif v is None:
                cells.append("   .")
            else:
                cells.append(f"{v:>4}")
        out.append(f"{label} | " + " ".join(cells))
    print("\n".join(out))
    sys.stdout.flush()


def knapsack(n, W, items, mode, title="", delay=0.03):
    """mode: 'live' (frame per cell), 'rows' (frame per item row), 'off'."""
    dp = [[None] * (W + 1) for _ in range(n + 1)]
    for c in range(W + 1):
        dp[0][c] = 0
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(W + 1):
            skip = dp[i - 1][c]
            if w <= c:
                take = dp[i - 1][c - w] + v
                dp[i][c] = max(skip, take)
                note = (f"{title} | item {i}: w={w}, v={v} | cap={c}: "
                        f"max(skip={skip}, take={dp[i-1][c-w]}+{v}={take}) = {dp[i][c]}")
            else:
                dp[i][c] = skip
                note = f"{title} | item {i}: w={w} > cap={c} -> skip = {skip}"
            if mode == "live":
                render(dp, items, W, i, c, note, clear=True)
                time.sleep(delay)
        if mode == "rows":
            render(dp, items, W, i, W, f"{title} | after item {i} (w={w}, v={v})", clear=False)
            print()

    chosen, c = [], W          # backtrack to find which items were taken
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i)
            c -= items[i - 1][0]
    chosen.reverse()
    return dp[n][W], chosen


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--fast" in sys.argv:
        mode = "off"
    elif sys.stdout.isatty():
        mode = "live"
    else:
        mode = "rows"

    cases, source = load_cases(args[0] if args else INPUT)
    print(f"Data source: {source} | {len(cases)} test cases\n")

    lines = []
    for idx, (n, W, items) in enumerate(cases, 1):
        best, chosen = knapsack(n, W, items, mode, title=f"#Test {idx}")
        if mode != "off":
            print(f">>> #Test {idx}: best value = {best}, items chosen = {chosen}\n")
            if mode == "live":
                time.sleep(1.0)
        lines.append(f"#Test{idx} input ({n} {W})  result: {best}")

    print("\n".join(lines))
    try:
        with open(OUTPUT, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\nSaved to {OUTPUT}")
    except OSError:
        print("\n(Could not write result.txt in this environment; results are printed above.)")


if __name__ == "__main__":
    main()
