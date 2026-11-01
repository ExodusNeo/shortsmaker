---
type: community
members: 8
---

# FeedbackTests

**Members:** 8 nodes

## Members
- [[dot-entry()]] - code - tests/test_quality.py
- [[dot-setUp()_4]] - code - tests/test_quality.py
- [[dot-test_logbook_is_never_modified_and_summary_is_returned()]] - code - tests/test_quality.py
- [[dot-test_other_channels_low_views_and_absent_active_entries_are_excluded()]] - code - tests/test_quality.py
- [[dot-test_posting_age_does_not_claim_metrics_age()]] - code - tests/test_quality.py
- [[dot-test_report_reason_cannot_become_a_lesson()]] - code - tests/test_quality.py
- [[dot-test_three_distinct_shorts_needed_and_duplicate_drops_count_once()]] - code - tests/test_quality.py
- [[FeedbackTests]] - code - tests/test_quality.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FeedbackTests
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_subprocess]]

## Top bridge nodes
- [[FeedbackTests]] - degree 8, connects to 1 community