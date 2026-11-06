---
type: community
members: 12
---

# FeedbackTests

**Members:** 12 nodes

## Members
- [[dot-entry()]] - code - tests/test_quality.py
- [[dot-setUp()_5]] - code - tests/test_quality.py
- [[dot-test_logbook_is_never_modified_and_has_no_retention_summary()]] - code - tests/test_quality.py
- [[dot-test_logbook_views_do_not_gate_retention()]] - code - tests/test_quality.py
- [[dot-test_missing_or_unreadable_reports_are_skipped()]] - code - tests/test_quality.py
- [[dot-test_planner_gets_retention_without_logbook_results()]] - code - tests/test_quality.py
- [[dot-test_posting_age_does_not_claim_metrics_age()]] - code - tests/test_quality.py
- [[dot-test_report_reason_cannot_become_a_lesson()]] - code - tests/test_quality.py
- [[dot-test_reviews_are_used_without_logbook_and_other_channels_are_excluded()]] - code - tests/test_quality.py
- [[dot-test_seo_gets_retention_without_logbook_results()]] - code - tests/test_quality.py
- [[dot-test_three_distinct_shorts_needed_and_duplicate_drops_count_once()]] - code - tests/test_quality.py
- [[FeedbackTests]] - code - tests/test_quality.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FeedbackTests
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_pathlib]]

## Top bridge nodes
- [[FeedbackTests]] - degree 12, connects to 1 community