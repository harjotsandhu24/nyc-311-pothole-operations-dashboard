# Data source

**Dataset:** NYC 311 Service Requests from 2020 to Present
**Publisher:** NYC Open Data (Department of Information Technology & Telecommunications)
**Dataset page:** https://data.cityofnewyork.us/d/erm2-nwe9

## What's in this folder

| File | What it is |
|---|---|
| `raw_311_export.csv` | The export downloaded from the dataset above, already filtered on NYC Open Data's site to Agency = DOT, Borough = Brooklyn, Descriptor = Pothole. 8,574 rows. |
| `scoped_2025_brooklyn_pothole.csv` | Output of `analysis/phase1b_filter.py` — the raw export narrowed to the exact analytical scope (see below). 8,531 rows. This is the dataset every other script and the dashboard numbers are built from. |
| `valid_closures.csv` | Output of `analysis/phase3_time_to_close.py` — the subset of scoped records with a usable Created/Closed date pair, used only for the time-to-close calculation. 8,508 rows. |

## Scope definition

The analysis is scoped to:
- Agency = DOT
- Borough = BROOKLYN
- Problem (Complaint Type) = Street Condition
- Problem Detail (Descriptor) = Pothole
- Created Date within calendar year 2025 (>= 2025-01-01 and < 2026-01-01)

The raw export already matched DOT / Brooklyn / Pothole at the portal level, but
still contained 40 rows tagged "Bridge Condition" (a different Problem type
under the same Pothole descriptor) and 3 rows created on 2026-01-01. The
`phase1b_filter.py` script removes those 43 rows to reach the final 8,531-row
scope, which is what the dashboard reports as "8,574 raw records → 8,531
analyzed."

## Regenerating the data

`scoped_2025_brooklyn_pothole.csv` and `valid_closures.csv` are both
regenerated automatically by the scripts in `analysis/` — see the main
README for run instructions. They're committed here so the dashboard
numbers can be checked without having to run the pipeline first.
