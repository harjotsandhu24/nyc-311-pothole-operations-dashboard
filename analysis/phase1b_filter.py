"""
Phase 1b — Scope filter.

Applies the analytical scope (DOT, Brooklyn, Street Condition,
Pothole, created in calendar year 2025) and writes the filtered
dataset used for every downstream step. This is the step that turns
8,574 raw rows into the 8,531 analyzed in the dashboard.

Run from the analysis/ directory: python phase1b_filter.py
"""
import pandas as pd

df = pd.read_csv('../data/raw_311_export.csv', dtype=str)
df['Created Date'] = pd.to_datetime(df['Created Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Closed Date'] = pd.to_datetime(df['Closed Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

scoped = df[
    (df['Agency'] == 'DOT') &
    (df['Borough'] == 'BROOKLYN') &
    (df['Problem (formerly Complaint Type)'] == 'Street Condition') &
    (df['Problem Detail (formerly Descriptor)'] == 'Pothole') &
    (df['Created Date'] >= '2025-01-01') &
    (df['Created Date'] < '2026-01-01')
].copy()

print("Scoped count:", len(scoped))
print("Expected: 8531")
print("Match:", len(scoped) == 8531)

print("\nStatus distribution in scope:")
print(scoped['Status'].value_counts())

scoped.to_csv('../data/scoped_2025_brooklyn_pothole.csv', index=False)
