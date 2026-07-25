# HN Evidence — python-bisect-score-boundary-lab

Source story: **"Using Python's Bisect Module"**
HN item ID: `25174048`
URL: https://news.ycombinator.com/item?id=25174048
Submitted by: `kaunta`
Time: 2020-11-21

Retrieval command:
```
hackernews get-item --id 25174048
```

Full story JSON: `hn_story_25174048.json`
Comment export: `hn_evidence.jsonl`

## Summary of claims (attributed)

**Linked article** (John Lekberg, https://johnlekberg.com/blog/2020-11-21-stdlib-bisect.html):
- The `bisect` module allows efficient search and update of sorted lists.
- `bisect.bisect` implements binary search for statistical data binning.
- `bisect.insort` inserts into a sorted list (insertion-sort style).
- For binning n records into m bins, the naive if-statement approach is O(m·n); dict lookup is O(m+n); `bisect.bisect` is O(m + n log m).
- The module provides four public functions.

**Commenter `snicker7`** (25175774):
- "The entire bisect module, consisting of 4 public functions, is literally only 32 lines of code."

**Commenter `rahimnathwani`** (25175793):
- Links to CPython source: https://github.com/python/cpython/blob/master/Lib/bisect.py

**Commenter `alexchamberlain`** (25176313):
- "most of it is replaced by a C implementation instead."

**Commenter `zhd`** (25177161):
- "Bisect is nice, but it's not the fastest option."
- For binning, suggests discretizing + dict lookup.
- "For insort, and indeed anything with sorted collections, just use the sortedcontainers module. Inserting an element is worst-case sublinear time, and also faster than C-extensions."

**Commenter `dmurray`** (25177576):
- "Is O(n + log n) really a thing or should he just write O(n)?"

**Commenter `Spivak`** (25177856):
- O(n + log n) simplifies to O(n) asymptotically, but the more detailed form can be illustrative.

**Commenter `kaunta`** (25181846, article author):
- "I should just write O(n). Thanks for catching the mistake, @dmurray. I'll fix that."

---

**Separation note:** The above claims are from the HN thread and linked article. Python standard library documentation describes the actual behavior of `bisect_left`, `bisect_right`, `insort_left`, and `insort_right`, including the `key=` parameter (Python 3.10+). Local observations from this lab are in `observations.json` and `RESULTS.md`.
