#!/usr/bin/env python3
"""unittest suite for python-bisect-score-boundary-lab"""

import bisect
import unittest

SCORES = [0.1, 0.3, 0.5, 0.5, 0.5, 0.7, 0.9]
THRESHOLD = 0.5

RECORDS_BASE = [
    {"score": 0.1, "name": "r0"},
    {"score": 0.3, "name": "r1"},
    {"score": 0.5, "name": "r2"},
    {"score": 0.5, "name": "r3"},
    {"score": 0.7, "name": "r4"},
]

RECORD_KEY = lambda record: record["score"]


class BisectScoreBoundaryLabTest(unittest.TestCase):

    def test_bisect_left_index_exact(self):
        """exact bisect_left index"""
        idx = bisect.bisect_left(SCORES, THRESHOLD)
        self.assertEqual(idx, 2)

    def test_bisect_right_index_exact(self):
        """exact bisect_right index"""
        idx = bisect.bisect_right(SCORES, THRESHOLD)
        self.assertEqual(idx, 5)

    def test_left_partition_lt(self):
        """left-partition: values before bisect_left index are < threshold"""
        idx = bisect.bisect_left(SCORES, THRESHOLD)
        self.assertTrue(all(v < THRESHOLD for v in SCORES[:idx]))

    def test_left_partition_ge(self):
        """left-partition: values from bisect_left index onward are >= threshold"""
        idx = bisect.bisect_left(SCORES, THRESHOLD)
        self.assertTrue(all(v >= THRESHOLD for v in SCORES[idx:]))

    def test_right_partition_le(self):
        """right-partition: values before bisect_right index are <= threshold"""
        idx = bisect.bisect_right(SCORES, THRESHOLD)
        self.assertTrue(all(v <= THRESHOLD for v in SCORES[:idx]))

    def test_right_partition_gt(self):
        """right-partition: values from bisect_right index onward are > threshold"""
        idx = bisect.bisect_right(SCORES, THRESHOLD)
        self.assertTrue(all(v > THRESHOLD for v in SCORES[idx:]))

    def test_keyed_search_numeric_value(self):
        """keyed search with a numeric search value"""
        records = [r.copy() for r in RECORDS_BASE]
        search_value = 0.5
        idx = bisect.bisect_left(records, search_value, key=RECORD_KEY)
        self.assertEqual(idx, 2)

    def test_key_not_called_on_numeric_search_value(self):
        """record key function is not called on the numeric search value"""
        records = [r.copy() for r in RECORDS_BASE]
        search_value = 0.5
        key_calls = []

        def tracking_key(record):
            key_calls.append(record)
            return record["score"]

        idx = bisect.bisect_left(records, search_value, key=tracking_key)
        # key() should only be called on dict records, never on the float search_value
        self.assertTrue(all(isinstance(c, dict) for c in key_calls),
                        f"key() was called on non-dict: {key_calls}")

    def test_insort_right_position_after_equals(self):
        """exact insertion position after all existing equal-score records"""
        records = [r.copy() for r in RECORDS_BASE]
        new_record = {"score": 0.5, "name": "new"}
        bisect.insort_right(records, new_record.copy(), key=RECORD_KEY)
        names = [r["name"] for r in records]
        insert_pos = names.index("new")
        self.assertEqual(insert_pos, 4)

    def test_existing_equal_score_order_preserved(self):
        """preservation of the existing equal-score record order"""
        records = [r.copy() for r in RECORDS_BASE]
        new_record = {"score": 0.5, "name": "new"}
        bisect.insort_right(records, new_record.copy(), key=RECORD_KEY)
        names = [r["name"] for r in records]
        # r2 and r3 should remain in order, before "new"
        self.assertLess(names.index("r2"), names.index("r3"))
        self.assertLess(names.index("r3"), names.index("new"))

    def test_final_projected_scores_nondecreasing(self):
        """final nondecreasing projected-score sequence"""
        records = [r.copy() for r in RECORDS_BASE]
        new_record = {"score": 0.5, "name": "new"}
        bisect.insort_right(records, new_record.copy(), key=RECORD_KEY)
        projected = [r["score"] for r in records]
        for i in range(len(projected) - 1):
            self.assertLessEqual(projected[i], projected[i + 1])

    def test_twelve_row_ordering_and_uniqueness(self):
        """deterministic twelve-row ordering and uniqueness"""
        from run_lab import run_lab
        rows = run_lab()
        self.assertEqual(len(rows), 12)
        keys = [(r["case"], r["method"]) for r in rows]
        self.assertEqual(len(keys), len(set(keys)), "duplicate (case, method) pairs")
        expected = [
            ("score_threshold_left_marker", "inspect_inputs"),
            ("score_threshold_left_marker", "execute_bisect"),
            ("score_threshold_left_marker", "verify_partition"),
            ("score_threshold_right_marker", "inspect_inputs"),
            ("score_threshold_right_marker", "execute_bisect"),
            ("score_threshold_right_marker", "verify_partition"),
            ("record_key_search_marker", "inspect_inputs"),
            ("record_key_search_marker", "execute_bisect"),
            ("record_key_search_marker", "verify_partition"),
            ("equal_score_insort_right_marker", "inspect_inputs"),
            ("equal_score_insort_right_marker", "execute_bisect"),
            ("equal_score_insort_right_marker", "verify_partition"),
        ]
        self.assertEqual(keys, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
