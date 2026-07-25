# python-bisect-score-boundary-lab

Tiny deterministic correctness lab for Python's stdlib `bisect` module, focused on ML-adjacent score boundary handling: duplicate thresholds, keyed score records, and deterministic equal-score insertion.

Inspired by the Hacker News thread ["Using Python's Bisect Module"](https://news.ycombinator.com/item?id=25174048), discussing John Lekberg's blog post on statistical data binning and sorted list insertion with `bisect.bisect` / `bisect.insort`.

**HN evidence:** see `hn_evidence.md` / `hn_story_25174048.json` / `hn_evidence.jsonl`.
Retrieved via: `hackernews get-item --id 25174048`

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

Records use a `"name"` label field for identification only. Equal-score records are genuinely equal under `key=lambda record: record["score"]` — no tie-breaking ID key is used.

Note on `insort_right`: Python applies the key to the new record during the search step, then inserts the original record. This differs from keyed `bisect_left`, where a numeric search value is not transformed by the record key function.

## Run

```bash
python3 run_lab.py
python3 -m unittest test_lab -v
```

Output:
- `observations.json` — 12 rows with computed indices, partition checks, and insertion positions
- `RESULTS.md` — human-readable summary table

## Results

12 / 12 rows pass. See `RESULTS.md`.

## Limitations

This lab verifies four specific score-boundary behaviors with a single fixed input set. It does **not** prove:

- performance or time complexity claims
- thread safety
- calibration quality or general ranking correctness
- superiority over heaps, NumPy, databases, or third-party sorted collections (e.g. sortedcontainers)

This is a tiny correctness check, not a benchmark or general-purpose evaluation.
