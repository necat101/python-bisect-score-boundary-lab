# RESULTS.md — python-bisect-score-boundary-lab

Total rows: 12
Passed: 12
Failed: 0

| Case | Method | ok | Detail |
|---|---|---|---|
| score_threshold_left_marker | inspect_inputs | True | scores=[0.1, 0.3, 0.5, 0.5, 0.5, 0.7, 0.9], search=0.5 |
| score_threshold_left_marker | execute_bisect | True | bisect_left returned 2, expected 2 |
| score_threshold_left_marker | verify_partition | True | left_all_lt=True, right_all_ge=True |
| score_threshold_right_marker | inspect_inputs | True | scores=[0.1, 0.3, 0.5, 0.5, 0.5, 0.7, 0.9], search=0.5 |
| score_threshold_right_marker | execute_bisect | True | bisect_right returned 5, expected 5 |
| score_threshold_right_marker | verify_partition | True | left_all_le=True, right_all_gt=True |
| record_key_search_marker | inspect_inputs | True | records=['r0:0.1', 'r1:0.3', 'r2:0.5', 'r3:0.5', 'r4:0.7'], search=0.5 |
| record_key_search_marker | execute_bisect | True | bisect_left(records, 0.5, key=...) returned 2, expected 2; key_called_on_search_value=False |
| record_key_search_marker | verify_partition | True | left_all_lt=True, right_all_ge=True |
| equal_score_insort_right_marker | inspect_inputs | True | records=['r0:0.1', 'r1:0.3', 'r2:0.5', 'r3:0.5', 'r4:0.7'], new=new:0.5 |
| equal_score_insort_right_marker | execute_bisect | True | insort_right inserted at 4, expected 4; existing_order_preserved=True |
| equal_score_insort_right_marker | verify_partition | True | nondecreasing=True, after_existing_equals=True |
