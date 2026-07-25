#!/usr/bin/env python3
"""
python-bisect-score-boundary-lab — run_lab.py

Four deterministic cases × three methods = twelve rows.
All observations are derived from actual bisect results.
"""

import bisect
import json

# Fixed sorted score list with duplicate 0.5 values
SCORES = [0.1, 0.3, 0.5, 0.5, 0.5, 0.7, 0.9]
THRESHOLD = 0.5

# Fixed list of score-keyed records, sorted by score
RECORDS_BASE = [
    {"score": 0.1, "name": "r0"},
    {"score": 0.3, "name": "r1"},
    {"score": 0.5, "name": "r2"},
    {"score": 0.5, "name": "r3"},
    {"score": 0.7, "name": "r4"},
]

RECORD_KEY = lambda record: record["score"]

# ---------------------------------------------------------------------------
# Inspect-input helpers (used by inspect_inputs rows AND by tests)
# ---------------------------------------------------------------------------

def check_scores_sorted_nondecreasing(scores):
    return all(scores[i] <= scores[i + 1] for i in range(len(scores) - 1))

def check_duplicate_block(scores, value):
    count = scores.count(value)
    return count >= 2

def check_records_have_score_and_name(records):
    return all(isinstance(r, dict) and "score" in r and "name" in r for r in records)

def check_records_nondecreasing_by_score(records):
    projected = [r["score"] for r in records]
    return all(projected[i] <= projected[i + 1] for i in range(len(projected) - 1))

def check_search_value_is_numeric(sv):
    return isinstance(sv, (int, float)) and not isinstance(sv, bool)

def check_key_ignores_name_field(key_fn):
    """Verify key() produces equal results for records that differ only in name."""
    a = {"score": 0.5, "name": "x"}
    b = {"score": 0.5, "name": "y"}
    return key_fn(a) == key_fn(b) == 0.5

# ---------------------------------------------------------------------------
# Case 1: score_threshold_left_marker
# ---------------------------------------------------------------------------

def case_score_threshold_left_marker():
    rows = []

    # inspect_inputs
    scores = SCORES[:]
    search_value = THRESHOLD
    sorted_ok = check_scores_sorted_nondecreasing(scores)
    search_is_05 = (search_value == 0.5)
    has_dup_block = check_duplicate_block(scores, search_value)
    ok = sorted_ok and search_is_05 and has_dup_block
    rows.append({
        "case": "score_threshold_left_marker",
        "method": "inspect_inputs",
        "scores": scores,
        "search_value": search_value,
        "sorted_ok": sorted_ok,
        "search_is_05": search_is_05,
        "has_dup_block": has_dup_block,
        "ok": ok,
        "detail": f"sorted_ok={sorted_ok}, search_is_05={search_is_05}, has_dup_block={has_dup_block}",
    })

    # execute_bisect
    idx = bisect.bisect_left(scores, search_value)
    expected_idx = 2  # first 0.5 in SCORES
    ok = (idx == expected_idx)
    rows.append({
        "case": "score_threshold_left_marker",
        "method": "execute_bisect",
        "index": idx,
        "expected_index": expected_idx,
        "ok": ok,
        "detail": f"bisect_left returned {idx}, expected {expected_idx}",
    })

    # verify_partition
    left_ok = all(v < search_value for v in scores[:idx])
    right_ok = all(v >= search_value for v in scores[idx:])
    ok = left_ok and right_ok
    rows.append({
        "case": "score_threshold_left_marker",
        "method": "verify_partition",
        "index": idx,
        "left_all_lt": left_ok,
        "right_all_ge": right_ok,
        "ok": ok,
        "detail": f"left_all_lt={left_ok}, right_all_ge={right_ok}",
    })

    return rows, idx

# ---------------------------------------------------------------------------
# Case 2: score_threshold_right_marker
# ---------------------------------------------------------------------------

def case_score_threshold_right_marker():
    rows = []

    # inspect_inputs
    scores = SCORES[:]
    search_value = THRESHOLD
    sorted_ok = check_scores_sorted_nondecreasing(scores)
    search_is_05 = (search_value == 0.5)
    has_dup_block = check_duplicate_block(scores, search_value)
    ok = sorted_ok and search_is_05 and has_dup_block
    rows.append({
        "case": "score_threshold_right_marker",
        "method": "inspect_inputs",
        "scores": scores,
        "search_value": search_value,
        "sorted_ok": sorted_ok,
        "search_is_05": search_is_05,
        "has_dup_block": has_dup_block,
        "ok": ok,
        "detail": f"sorted_ok={sorted_ok}, search_is_05={search_is_05}, has_dup_block={has_dup_block}",
    })

    # execute_bisect
    idx = bisect.bisect_right(scores, search_value)
    expected_idx = 5  # after last 0.5 in SCORES
    ok = (idx == expected_idx)
    rows.append({
        "case": "score_threshold_right_marker",
        "method": "execute_bisect",
        "index": idx,
        "expected_index": expected_idx,
        "ok": ok,
        "detail": f"bisect_right returned {idx}, expected {expected_idx}",
    })

    # verify_partition
    left_ok = all(v <= search_value for v in scores[:idx])
    right_ok = all(v > search_value for v in scores[idx:])
    ok = left_ok and right_ok
    rows.append({
        "case": "score_threshold_right_marker",
        "method": "verify_partition",
        "index": idx,
        "left_all_le": left_ok,
        "right_all_gt": right_ok,
        "ok": ok,
        "detail": f"left_all_le={left_ok}, right_all_gt={right_ok}",
    })

    return rows, idx

# ---------------------------------------------------------------------------
# Case 3: record_key_search_marker
# ---------------------------------------------------------------------------

def case_record_key_search_marker():
    rows = []

    records = [r.copy() for r in RECORDS_BASE]
    search_value = 0.5  # numeric, not a record dict

    # inspect_inputs
    records_nondecreasing = check_records_nondecreasing_by_score(records)
    records_have_fields = check_records_have_score_and_name(records)
    search_is_numeric = check_search_value_is_numeric(search_value)
    ok = records_nondecreasing and records_have_fields and search_is_numeric
    rows.append({
        "case": "record_key_search_marker",
        "method": "inspect_inputs",
        "records": records,
        "search_value": search_value,
        "key": "lambda record: record[\"score\"]",
        "records_nondecreasing": records_nondecreasing,
        "records_have_fields": records_have_fields,
        "search_is_numeric": search_is_numeric,
        "ok": ok,
        "detail": f"records_nondecreasing={records_nondecreasing}, records_have_fields={records_have_fields}, search_is_numeric={search_is_numeric}",
    })

    # Track whether key() is called on the numeric search_value.
    # Python's bisect key= applies the key to list elements only, not to x.
    key_calls = []

    def tracking_key(record):
        key_calls.append(record)
        try:
            return record["score"]
        except (TypeError, KeyError):
            # If bisect ever called key() on the numeric search_value,
            # record["score"] would fail. In that case, record this.
            key_calls.append("__search_value_key_call__")
            raise

    try:
        idx = bisect.bisect_left(records, search_value, key=tracking_key)
        key_called_on_search_value = "__search_value_key_call__" in key_calls
    except Exception:
        idx = -1
        key_called_on_search_value = True

    # Verify key was NOT called on the numeric search_value
    # (all key_calls should be dict records from the list)
    key_only_on_records = all(isinstance(c, dict) for c in key_calls)
    expected_idx = 2  # first 0.5 record (r2)
    ok = (idx == expected_idx) and key_only_on_records and not key_called_on_search_value

    rows.append({
        "case": "record_key_search_marker",
        "method": "execute_bisect",
        "index": idx,
        "expected_index": expected_idx,
        "key_called_on_search_value": key_called_on_search_value,
        "key_only_on_records": key_only_on_records,
        "ok": ok,
        "detail": f"bisect_left(records, {search_value}, key=...) returned {idx}, expected {expected_idx}; key_called_on_search_value={key_called_on_search_value}",
    })

    # verify_partition
    projected = [r["score"] for r in records]
    left_ok = all(v < search_value for v in projected[:idx])
    right_ok = all(v >= search_value for v in projected[idx:])
    ok = left_ok and right_ok
    rows.append({
        "case": "record_key_search_marker",
        "method": "verify_partition",
        "index": idx,
        "projected_scores": projected,
        "left_all_lt": left_ok,
        "right_all_ge": right_ok,
        "ok": ok,
        "detail": f"left_all_lt={left_ok}, right_all_ge={right_ok}",
    })

    return rows, idx

# ---------------------------------------------------------------------------
# Case 4: equal_score_insort_right_marker
# ---------------------------------------------------------------------------

def case_equal_score_insort_right_marker():
    rows = []

    records = [r.copy() for r in RECORDS_BASE]
    new_record = {"score": 0.5, "name": "new"}

    # inspect_inputs
    records_nondecreasing = check_records_nondecreasing_by_score(records)
    new_score_is_05 = (new_record.get("score") == 0.5)
    # Verify existing equal-score names are in expected order (r2 then r3)
    names = [r.get("name") for r in records]
    existing_equal_order_ok = (
        "r2" in names and "r3" in names
        and names.index("r2") < names.index("r3")
    )
    key_ignores_name = check_key_ignores_name_field(RECORD_KEY)
    ok = records_nondecreasing and new_score_is_05 and existing_equal_order_ok and key_ignores_name
    rows.append({
        "case": "equal_score_insort_right_marker",
        "method": "inspect_inputs",
        "records_before": [r.copy() for r in records],
        "new_record": new_record.copy(),
        "key": "lambda record: record[\"score\"]",
        "records_nondecreasing": records_nondecreasing,
        "new_score_is_05": new_score_is_05,
        "existing_equal_order_ok": existing_equal_order_ok,
        "key_ignores_name": key_ignores_name,
        "ok": ok,
        "detail": f"records_nondecreasing={records_nondecreasing}, new_score_is_05={new_score_is_05}, existing_equal_order_ok={existing_equal_order_ok}, key_ignores_name={key_ignores_name}",
    })

    # execute_bisect (insort_right)
    # insort_right applies key to the new record during search,
    # then inserts the original record object.
    records_copy = [r.copy() for r in records]
    bisect.insort_right(records_copy, new_record.copy(), key=RECORD_KEY)

    # Find where new_record landed
    try:
        insert_pos = [r["name"] for r in records_copy].index("new")
    except ValueError:
        insert_pos = -1

    # Expected: after r2 and r3 (the two existing 0.5 records)
    # RECORDS_BASE: r0(0.1), r1(0.3), r2(0.5), r3(0.5), r4(0.7)
    # After insort_right: r0, r1, r2, r3, new, r4
    expected_pos = 4
    existing_equal_names_before = ["r2", "r3"]
    names_before_insert = [r["name"] for r in records_copy[:insert_pos]]
    existing_order_preserved = (
        existing_equal_names_before[0] in names_before_insert
        and existing_equal_names_before[1] in names_before_insert
        and names_before_insert.index("r2") < names_before_insert.index("r3")
    )

    ok = (insert_pos == expected_pos) and existing_order_preserved
    rows.append({
        "case": "equal_score_insort_right_marker",
        "method": "execute_bisect",
        "insert_pos": insert_pos,
        "expected_pos": expected_pos,
        "existing_order_preserved": existing_order_preserved,
        "records_after_names": [r["name"] for r in records_copy],
        "ok": ok,
        "detail": f"insort_right inserted at {insert_pos}, expected {expected_pos}; existing_order_preserved={existing_order_preserved}",
    })

    # verify_partition
    projected = [r["score"] for r in records_copy]
    nondecreasing = all(projected[i] <= projected[i + 1] for i in range(len(projected) - 1))
    # Verify new record is after existing equal-score records
    names = [r["name"] for r in records_copy]
    new_idx = names.index("new")
    r2_idx = names.index("r2")
    r3_idx = names.index("r3")
    after_existing_equals = (new_idx > r2_idx) and (new_idx > r3_idx)
    ok = nondecreasing and after_existing_equals

    rows.append({
        "case": "equal_score_insort_right_marker",
        "method": "verify_partition",
        "projected_scores": projected,
        "nondecreasing": nondecreasing,
        "after_existing_equals": after_existing_equals,
        "ok": ok,
        "detail": f"nondecreasing={nondecreasing}, after_existing_equals={after_existing_equals}",
    })

    return rows, insert_pos

# ---------------------------------------------------------------------------
# Lab runner
# ---------------------------------------------------------------------------

def run_lab():
    all_rows = []
    for case_fn in [
        case_score_threshold_left_marker,
        case_score_threshold_right_marker,
        case_record_key_search_marker,
        case_equal_score_insort_right_marker,
    ]:
        rows, _ = case_fn()
        all_rows.extend(rows)

    assert len(all_rows) == 12, f"expected 12 rows, got {len(all_rows)}"
    # Check ordering and uniqueness
    keys = [(r["case"], r["method"]) for r in all_rows]
    assert keys == sorted(set(keys), key=lambda k: (
        ["score_threshold_left_marker", "score_threshold_right_marker",
         "record_key_search_marker", "equal_score_insort_right_marker"].index(k[0]),
        ["inspect_inputs", "execute_bisect", "verify_partition"].index(k[1])
    )), "row ordering mismatch"
    assert len(keys) == len(set(keys)), "duplicate (case, method) pairs"

    return all_rows

if __name__ == "__main__":
    rows = run_lab()
    with open("observations.json", "w") as f:
        json.dump(rows, f, indent=2)

    # RESULTS.md
    passed = sum(1 for r in rows if r["ok"])
    with open("RESULTS.md", "w") as f:
        f.write("# RESULTS.md — python-bisect-score-boundary-lab\n\n")
        f.write(f"Total rows: {len(rows)}\n")
        f.write(f"Passed: {passed}\n")
        f.write(f"Failed: {len(rows) - passed}\n\n")
        f.write("| Case | Method | ok | Detail |\n")
        f.write("|---|---|---|---|\n")
        for r in rows:
            detail = r["detail"].replace("|", "\\|")
            f.write(f"| {r['case']} | {r['method']} | {r['ok']} | {detail} |\n")

    print(f"observations.json: {len(rows)} rows, {passed} passed")
    print(f"RESULTS.md written")
