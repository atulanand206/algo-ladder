# Writing a lesson

Every topic in `catalog.txt` and `systems.txt` gets one lesson. A lesson explains the whole thing: what it is, how it is built,
how to think about it, and working code. Pilot examples to copy the quality from: `lessons/pilot.txt`
(`binary-search`, `dsu`, `dijkstra`, `knapsack`, `kmp`, `consistent`).

## File

Put lessons in `lessons/<area>.txt` (one file per area, for example `lessons/graph.txt`). One block per topic:

```
### topic-id
--idea
...
--build
...
--think
...
--cost
...
--java
...
--py
...
--cpp
...
```

`topic-id` must be an id from `catalog.txt` or `systems.txt`. All seven sections are required. `python3 check.py` fails otherwise.

## Sections

- **idea**: the concept in plain words, 2 short paragraphs. First: what problem it solves and the picture to hold in your head
  (an analogy is welcome). Second: why it works, or the one insight everything depends on. No jargon before it is explained.
- **build**: a numbered list (`1. `) of the steps to construct it, in the order you would do them. Someone who reads only this
  should be able to rebuild it from scratch. Name the variables used in the code.
- **think**: a bullet list (`- `). Cover: the signal in a problem statement that says "use this"; what to decide first;
  the neighbouring techniques and when to choose them instead; the common mistakes (off-by-one, overflow, wrong direction).
  This is the algorithm thought process, and it is the part learners value most.
- **cost**: one or two sentences. Time, space, and the condition it depends on.
- **java / py / cpp**: complete, runnable **methods** (not loose statements), the same algorithm in all three, with short
  comments on the lines that carry the idea. Use the helper names from the code pieces where one exists (`find`, `powMod`).
  Keep each under about 45 lines. Each language must be idiomatic, not a transliteration.

## Build on the code pieces (required)

The site is layered: small **code pieces** (`snips/*.txt`, the method forms in `snips/z1.txt` and `snips/z2.txt`) are the lowest layer, and algorithms are
built by calling them. A lesson must **call** the pieces it is built on, not re-implement them inline.

1. Run `python3 pieces.py <topic-id>`. It lists the pieces linked to that topic, the exact method names to call in each language
   (they differ: `push_pq` in Python, `pushPq` in Java and C++), and the piece's code.
2. Call those methods in your Java, Python and C++. Do not paste the piece's body into your lesson. If the piece is missing something you
   need, say so in your final report instead of inventing a second copy.
3. Add an optional section `--uses` listing the piece ids you call, one per line (for example `u-pq` then `u-relax`).
   Mention in `--build` where each piece is used ("step 4 calls `relax`"), so the layering is visible to the learner.
4. Pieces of your own that no earlier piece covers (a new helper that only this algorithm needs) can be defined in the lesson itself.
5. A lesson for an algorithm built on other **algorithms** (for example Dijkstra on a heap) should name them in `--build` and use their
   standard form rather than a new one.

`python3 check.py` fails if `--uses` lists something that is not a piece, or if any of the three languages never calls it, and it
reports how many lessons with linked pieces actually build on them. Aim for all of them.

## Style

- Plain English, short sentences, no em dashes. Explain every term the first time it appears.
- Inline code goes in backticks. Lists are `- ` or `1. ` lines. Blank line or a new line starts a new paragraph.
- Be exact: a lesson that is confidently wrong is worse than none. Check the complexity and the edge cases.
- Complex topics (flows, suffix structures, FFT, DP optimisations): split the explanation into small steps in `build`, and say
  in `think` what the invariant is and why each step keeps it true.
- Real systems (`systems.txt`): `idea` says what the product does, `build` walks through how the algorithms combine inside it
  (name the algorithm topics it uses), `think` covers the design trade-offs, and the code is a small working model of the core.

## Check

```bash
python3 build.py && python3 check.py
```

`check.py` prints how many topics have a lesson. Compile or run the code you wrote before committing it.
