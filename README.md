# Algo Ladder

**Every algorithm, built from the one below.**

A free, graphical map of 459 algorithms, data structures and the real-world systems built on them. Every lesson is made from small code pieces in Java, Python and C++, on a map you can walk, with verified practice problems from Codeforces, CSES and AtCoder. 59 small levels, a "find the technique" search for when you are stuck on a problem, and progress that you can move between devices with a short code.

Spot a mistake or want a problem added? [Open an issue](https://github.com/atulanand206/algo-ladder/issues/new).

## How it is built

The site is one static page (`app.html`) that loads its content from JSON files in `data/`.

| Source file | What it holds |
|---|---|
| `catalog.txt` | Algorithms and data structures: `id\|name\|tier\|area\|needs\|meaning` |
| `systems.txt` | Real systems and the algorithms behind them (same format) |
| `utils_extra.txt`, `utils_links.txt`, `tree.py` | Code pieces and which algorithms use them |
| `snips/*.txt` | The code for each piece, in three languages |
| `content.py`, `inventory.csv` | Variants, walkthroughs and the problem list |

```bash
python3 build.py   # writes dist/ (index.html and dist/data/*.json)
python3 check.py   # validates links, snippets and the public build
cd dist && python3 -m http.server 8000
```

Pushes to `main` run `.github/workflows/pages.yml`: build, check, then deploy to GitHub Pages.
Progress is saved in the visitor's own browser.

## Adding content

- New topic: add a line to `catalog.txt` (or `systems.txt`) with its prerequisites. The build fails if a link or tier is wrong.
- New code piece: add it to `utils_extra.txt` and a block to a file in `snips/`. `check.py` fails if a snippet is missing.
