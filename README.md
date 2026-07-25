# python-bisect-score-boundary-lab

Tiny deterministic correctness lab for Python's stdlib `bisect` module, focused on ML-adjacent score boundary handling: duplicate thresholds, keyed score records, and deterministic equal-score insertion.

## Background

### Linked article

John Lekberg, ["Using Python's Bisect Module"](https://johnlekberg.com/blog/2020-11-21-stdlib-bisect.html) (2020-11-21):
- The `bisect` module allows efficient search and update of sorted lists.
- `bisect.bisect` implements binary search for statistical data binning.
- `bisect.insort` inserts into a sorted list (insertion-sort style).
- For binning n records into m bins, the naive if-statement approach is O(m·n); dict lookup is O(m+n); `bisect.bisect` is O(m + n log m).
- The module provides four public functions.

### Hacker News discussion

[Hacker News thread](https://news.ycombinator.com/item?id=25174048) — "Using Python's Bisect Module" — submitted by `kaunta`.

Named commenter claims:
- `snicker7` (25175774): "The entire bisect module, consisting of 4 public functions, is literally only 32 lines of code."
- `rahimnathwani` (25175793): Links to CPython source: https://github.com/python/cpython/blob/master/Lib/bisect.py
- `alexchamberlain` (25176313): "most of it is replaced by a C implementation instead."
- `zhd` (25177161): "Bisect is nice, but it's not the fastest option." Suggests discretizing + dict lookup for binning; "For insort, … just use the sortedcontainers module. Inserting an element is worst-case sublinear time, and also faster than C-extensions."
- `dmurray` (25177576): "Is O(n + log n) really a thing or should he just write O(n)?"
- `Spivak` (25177856): O(n + log n) simplifies to O(n) asymptotically, but the more detailed form can be illustrative.
- `kaunta` (25181846, article author): "I should just write O(n). Thanks for catching the mistake, @dmurray. I'll fix that."

Full HN evidence: see `hn_evidence.md` / `hn_story_25174048.json` / `hn_evidence.jsonl`.
Retrieved via: `hackernews get-item --id 25174048`

### Python documentation

Python standard library documentation for [`bisect`](https://docs.python.org/3/library/bisect.html) (Python 3.10+):

- `bisect_left(a, x, lo=0, hi=None, *, key=None)` — Locate the insertion point for `x` in `a` to maintain sorted order. If `x` is already present in `a`, the insertion point will be before (to the left of) any existing entries. All values `a[i]` with `i < index` satisfy `a[i] < x`, and all `a[i]` with `i >= index` satisfy `a[i] >= x`.
- `bisect_right(a, x, lo=0, hi=None, *, key=None)` — Similar to `bisect_left()`, but returns an insertion point which comes after (to the right of) any existing entries of `x` in `a`. All values `a[i]` with `i < index` satisfy `a[i] <= x`, and all `a[i]` with `i >= index` satisfy `a[i] > x`.
- `insort_left(a, x, lo=0, hi=None, *, key=None)` — Insert `x` in `a` in sorted order, keeping `x` to the left of any existing equal entries.
- `insort_right(a, x, lo=0, hi=None, *, key=None)` — Insert `x` in `a` in sorted order, keeping `x` to the right of any existing equal entries.

Key-parameter behavior:
- For `bisect_left` / `bisect_right` with `key=`, the key function is applied to elements of the list `a` during the search. The search value `x` is compared directly against those projected keys and is **not** transformed by the key function.
- For `insort_left` / `insort_right` with `key=`, the key function is applied to the new element `x` during the search step, and the original (unkeyed) element is inserted into the list.

This distinction is the basis for the `record_key_search_marker` case in this lab.

## Scope

Four deterministic cases × three methods = **12 rows total**.

All with a fixed sorted score list containing duplicate `0.5` values. No randomness, no downloads, no third-party packages.

| Case | What it tests |
|---|---|
| `score_threshold_left_marker` | `bisect_left` returns the first duplicate position; partition: `< 0.5` before, `>= 0.5` after |
| `score_threshold_right_marker` | `bisect_right` returns the position after the duplicate block; partition: `<= 0.5` before, `> 0.5` after |
| `record_key_search_marker` | keyed `bisect_left` on score-keyed dict records with a numeric search value; the key function is applied to stored records but not to the search value |
| `equal_score_insort_right_marker` | `insort_right` with `key=lambda r: r["score"]`; new equal-score record inserts after existing equals; projected score sequence remains sorted |

Each case runs three methods: `inspect_inputs`, `execute_bisect`, `verify_partition`.

The `inspect_inputs` rows validate:
- left/right cases: score list is nondecreasing, search value is `0.5`, and the list contains a duplicate `0.5` block;
- keyed-search case: records are nondecreasing by projected score, every record has `score` and `name` fields, and the search value is numeric (not a record dict);
- insort case: existing records are nondecreasing, new record score is `0.5`, existing equal-score names are in expected order (`r2` before `r3`), and the key function ignores the label field.

Records use a `"name"` label field for identification only. Equal-score records are genuinely equal under `key=lambda record: record["score"]` — no tie-breaking ID key is used.

## Local observations

Running `python3 run_lab.py` produces 12 rows, all passing:
- `bisect_left([0.1, 0.3, 0.5, 0.5, 0.5, 0.7, 0.9], 0.5)` → index `2` (first duplicate)
- `bisect_right(..., 0.5)` → index `5` (after duplicate block)
- keyed `bisect_left` with numeric search value: key function is NOT called on the search value
- `insort_right` with equal-score record: inserted at position `4`, after existing equals, order preserved, score sequence remains nondecreasing

See `observations.json` and `RESULTS.md` for full details.

## Run

Linux / macOS:
```bash
./run.sh
```
Windows:
```bat
run.bat
```

Or manually:
```bash
python3 run_lab.py
python3 -m unittest test_lab -v
```

Output:
- `observations.json` — 12 rows with computed indices, partition checks, and insertion positions
- `RESULTS.md` — human-readable summary table

## Results

12 / 12 lab rows pass. `unittest` suite: 22 tests pass (12 behavioral + 10 inspect-input corruption tests).

## Non-claims and limitations

This lab verifies four specific score-boundary behaviors with a single fixed input set. It does **not** prove:

- performance or time complexity claims
- thread safety
- calibration quality or general ranking correctness
- superiority over heaps, NumPy, databases, or third-party sorted collections (e.g. sortedcontainers)

This is a tiny correctness check, not a benchmark or general-purpose evaluation.

Claims in the "Linked article" and "Hacker News discussion" sections above are attributed to their respective authors and are not endorsed by this lab. Python documentation claims are from the official Python standard library documentation. Local observations are from running the code in this repository.
