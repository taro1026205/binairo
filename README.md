# Binairo Solver

A puzzle solver for [Binairo](https://www.puzzle-binairo.com) implementing two search strategies with step-by-step visualization.

## Algorithms

**Blind Search — DFS with Backtracking**
Explores all possible cell assignments depth-first, backtracking on constraint violations.

**Heuristic Search — CSP**
Solves as a Constraint Satisfaction Problem using three mechanisms:
- Constraint Propagation — eliminates invalid values before branching
- Degree Heuristic — prioritizes cells with the most unfilled neighbors
- Early Pruning — detects dead ends before full assignment

## Project Structure

```
.
├── main.py              # Performance benchmark (runtime + memory)
├── gui.py               # Tkinter visualizer with step navigation
├── dfs.py               # DFS solver
├── heuristic.py         # Heuristic CSP solver
├── utils/
│   ├── binairo.py       # Base class, validation, logging
│   └── ioprocess.py     # Puzzle file reader
└── data/
    ├── 6x6.txt
    ├── 10x10.txt
    └── 14x14.txt
```

## Usage

**Run benchmark:**
```bash
python main.py
```

**Run visualizer:**
```bash
python gui.py
```

The visualizer supports manual stepping (`←` `→`) and auto-play (`Space`) through the solution history.

## Puzzle Format

Input files use space-separated values per row. Empty cells are represented as `.`, `_`, or `-1`.

```
. 1 . . 0 .
0 . . 1 . .
```

## Rules

- Fill the grid with `0`s and `1`s
- No more than two identical values may be adjacent horizontally or vertically
- Each row and column must contain an equal number of `0`s and `1`s
- All rows must be unique; all columns must be unique

---
