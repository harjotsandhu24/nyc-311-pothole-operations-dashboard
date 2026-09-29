# Methodology & findings

Full detail behind the numbers shown in the dashboard and summarized in the
top-level README. Every number below was recomputed directly from the CSV
using the scripts in `analysis/` — none of it is assumed or estimated.

## Scope definition

Agency == DOT, Borough == BROOKLYN, Problem == Street Condition,
Problem Detail == Pothole, Created Date within calendar year 2025
(>= 2025-01-01 and < 2026-01-01).

## Verified counts

- Raw file: 8,574 rows, 8,574 unique Unique Key values (0 duplicates)
- Agency: 100% DOT. Borough: 100% BROOKLYN. Problem Detail: 100% Pothole.
- Problem: 8,534 Street Condition, 40 Bridge Condition
- Date range in raw file: 2025-01-01 to 2026-01-01 (3 records land on 2026-01-01)
- Scope filter excludes 40 Bridge Condition + 3 records >= 2026-01-01
  (no overlap between these two groups) = 43 excluded
- Final scoped count: 8,531 (8,574 - 43) — matches the dashboard exactly
- Status in scope: 8,509 Closed / 15 Pending / 7 Open

## Data quality findings

| Issue | Affected records | Treatment | Reason |
|---|---|---|---|
| 40 Bridge Condition records tagged with the Pothole descriptor | 40 | Excluded by scope filter | Outside the chosen Street Condition definition, not evidence of bad data |
| Records created 2026-01-01 | 3 | Excluded by scope filter | Outside the chosen 2025 calendar-year window |
| Missing Incident Zip | 81 (0.9% of scope) | Retained in all totals, excluded only from ZIP-level breakdowns | Geography unknown, not erroneous |
| Closed Date earlier than Created Date (Unique Key 64345550, Created 2025-03-12 06:05:50, Closed 2025-03-12 05:45:00) | 1 | Excluded from time-to-close calculation only, retained in the Closed count | Inconsistent timestamp pair, not deletable without losing the otherwise-valid Closed status |
| Missing Closed Date despite non-Closed status (expected for Open/Pending) | 20 | Retained | Expected given the status |
| Open/Pending status but carries a Closed Date | 2 | Flagged, not used in time-to-close calc (status is not Closed) | Documented inconsistency, not corrected |

## Time-to-close calculation

Included only if: Status == Closed, Created Date present, Closed Date
present, Closed Date >= Created Date. 8,508 of 8,509 Closed records
qualify (1 excluded per the timestamp-inconsistency finding above).

- **Median: 21.52 hours (~0.90 days)** — the displayed metric
- Mean: 36.97 hours (~1.54 days) — diagnostic only, not displayed,
  inflated by outliers (11 requests over 30 days, max 367 days)

## Monthly volume (Created Date, 2025)

Jan 907, Feb 781, Mar 1,027, Apr 810, May 744, Jun 1,019, Jul 621,
Aug 618, Sep 499, Oct 514, Nov 393, Dec 598.

Highest: March (1,027). Lowest: November (393).

## ZIP-level distribution

38 distinct ZIP codes represented (81 records missing ZIP, excluded
from this breakdown only). Top ZIP: 11236 (379 requests, 4.4% of
scope). Median requests per ZIP: 213. No single ZIP dominates the
distribution — reliable enough to describe general concentration, not
precise enough for block-level claims given per-ZIP sample sizes.

## What this does and doesn't claim

No operational result, improvement percentage, causal explanation, or
business impact is claimed anywhere in this project. Every number above
is a direct count or calculation from the supplied CSV, reproducible by
running the scripts in `analysis/` in order.
