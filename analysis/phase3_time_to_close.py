"""
Phase 3 — Time-to-close calculation.

Restricts to records where the closure timestamps are actually usable
(Status == Closed, both dates present, Closed Date >= Created Date)
before computing a duration, so one bad timestamp pair can't skew the
headline number.

Run from the analysis/ directory: python phase3_time_to_close.py
"""
import pandas as pd

scoped = pd.read_csv('../data/scoped_2025_brooklyn_pothole.csv', dtype=str)
scoped['Created Date'] = pd.to_datetime(scoped['Created Date'])
scoped['Closed Date'] = pd.to_datetime(scoped['Closed Date'], errors='coerce')

valid_closure = scoped[
    (scoped['Status'] == 'Closed') &
    (scoped['Created Date'].notna()) &
    (scoped['Closed Date'].notna()) &
    (scoped['Closed Date'] >= scoped['Created Date'])
].copy()

excluded_closed = scoped[(scoped['Status'] == 'Closed')].shape[0] - valid_closure.shape[0]
print("Closed records:", (scoped['Status'] == 'Closed').sum())
print("Valid-closure records used for time to close:", len(valid_closure))
print("Excluded from Closed (missing date or negative duration):", excluded_closed)

valid_closure['duration_hours'] = (valid_closure['Closed Date'] - valid_closure['Created Date']).dt.total_seconds() / 3600
valid_closure['duration_days'] = valid_closure['duration_hours'] / 24

median_hours = valid_closure['duration_hours'].median()
mean_hours = valid_closure['duration_hours'].mean()
print(f"\nMedian time to close: {median_hours:.2f} hours ({median_hours/24:.2f} days)")
print(f"Mean time to close (diagnostic only): {mean_hours:.2f} hours ({mean_hours/24:.2f} days)")

print("\nDuration distribution (hours):")
print(valid_closure['duration_hours'].describe())

print("\nClosures within 1 hour:", (valid_closure['duration_hours'] < 1).sum())
print("Closures over 30 days:", (valid_closure['duration_days'] > 30).sum())
print("Closures over 90 days:", (valid_closure['duration_days'] > 90).sum())
print("Max duration (days):", valid_closure['duration_days'].max())

valid_closure.to_csv('../data/valid_closures.csv', index=False)
