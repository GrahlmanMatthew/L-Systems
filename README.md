# L-Systems

A Lindenmayer System visualiser — watch fractal plants grow branch by branch in real time.

![CI](https://github.com/GrahlmanMatthew/L-Systems/actions/workflows/ci.yml/badge.svg)
![GitHub release](https://img.shields.io/github/v/release/GrahlmanMatthew/L-Systems)

## Demo

<!-- Add demo GIF here before merging to main -->

## How it works

An L-System is a string-rewriting grammar. You start with a short axiom string (`X`) and a
set of production rules (`X → F+[[X]-X]-F[-FX]+X`, `F → FF`). Each iteration substitutes
every character in the current string using the rules — the string grows exponentially. After
a handful of iterations the string can represent millions of drawing instructions.

The string is then interpreted as turtle-drawing commands:

| Symbol | Meaning |
|--------|---------|
| `F`, `G` | Move forward one step, draw a line |
| `f` | Move forward one step, no line |
| `+` | Turn right by the preset's angle |
| `-` | Turn left by the preset's angle |
| `[` | Push current position and heading onto a stack (start a branch) |
| `]` | Pop position and heading from the stack (end a branch, return to fork) |

The branching stack (`[` / `]`) is what produces the tree-like structures. Every `[` forks a
new branch; every `]` jumps back to the fork point and continues from there. Tweaking the
angle by a few degrees or changing a single production rule produces completely different
organic shapes — from sparse trees to dense ferns to geometric snowflakes.

This visualiser pre-computes all segments from the expanded string and then renders them
one by one per frame, so you watch the whole structure emerge from a single point.

## Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) — install once via PowerShell (Windows):

  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

## Installation and setup

```bash
git clone https://github.com/GrahlmanMatthew/L-Systems.git
cd l-systems

uv venv
source .venv/Scripts/activate        # Windows (Git Bash)
# .venv\Scripts\Activate.ps1         # Windows (PowerShell — run once: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser)
# source .venv/bin/activate          # macOS / Linux

uv pip install -e ".[dev]"
```

> **Broken venv?** If you see `No Python at '...'` after a `uv` upgrade or Python re-install,
> delete and recreate the venv: `rm -rf .venv && uv venv && uv pip install -e ".[dev]"`

### Pre-commit hooks (first time only)

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
detect-secrets scan > .secrets.baseline
```

## Usage

```bash
python -m l_systems
```

### Controls

| Key | Action |
|-----|--------|
| `1` – `6` | Switch to preset |
| `Space` | Pause / resume animation |
| `R` | Restart current preset |
| `+` / `=` | Increase draw speed |
| `-` | Decrease draw speed |
| `S` | Save screenshot to `output/` |
| `Esc` | Quit |

## Configuration

Optional environment variables (copy `.env.example` to `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FPS_TARGET` | `60` | Target frames per second |
| `SEGMENTS_PER_FRAME` | `8` | Segments drawn per frame — controls animation speed |
| `DEBUG` | _(unset)_ | Set to any value to enable debug logging |

## Running the tests

```bash
pytest
```

Lint and format check:

```bash
ruff check src tests
ruff format --check src tests
```

---

© 2026 Matthew Grahlman. All rights reserved.
