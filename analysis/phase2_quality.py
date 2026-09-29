"""
Phase 2 — Data quality / validation checks.

Runs against the already-scoped dataset (not the raw file) and checks
for the kinds of problems that would make the numbers untrustworthy:
missing ZIPs, missing dates, and Closed Date / Created Date pairs
that don't make logical sense.

Run from the analysis/ directory: python phase2_quality.py
"""
import pandas as pd

scoped = pd.read_csv('../data/scoped_2025_brooklyn_pothole.csv', dtype=str)
scoped['Created Date'] = pd.to_datetime(scoped['Created Date'])
scoped['Closed Date'] = pd.to_datetime(scoped['Closed Date'], errors='coerce')

print("Duplicate Unique Keys:", len(scoped) - scoped['Unique Key'].nunique())
print("Missing Created Date:", scoped['Created Date'].isna().sum())
print("Missing Closed Date:", scoped['Closed Date'].isna().sum())
print("Missing Incident Zip:", scoped['Incident Zip'].isna().sum())

# Closed Date before Created Date
valid_both = scoped.dropna(subset=['Closed Date'])
before = valid_both[valid_both['Closed Date'] < valid_both['Created Date']]
print("\nClosed Date < Created Date count:", len(before))
print(before[['Unique Key', 'Created Date', 'Closed Date', 'Status']] if len(before) else "none")

same_day = valid_both[(valid_both['Closed Date'] - valid_both['Created Date']).dt.total_seconds() < 3600]
print("\nClosures within 1 hour:", len(same_day))

# Closed status but missing closed date
closed_missing_date = scoped[(scoped['Status'] == 'Closed') & (scoped['Closed Date'].isna())]
print("\nStatus=Closed but Closed Date missing:", len(closed_missing_date))

# Open/Pending but has closed date (inconsistent)
open_with_closed = scoped[(scoped['Status'].isin(['Open', 'Pending'])) & (scoped['Closed Date'].notna())]
print("Status=Open/Pending but has Closed Date:", len(open_with_closed))
