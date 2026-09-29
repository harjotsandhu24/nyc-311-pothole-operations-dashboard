"""
Phase 1 — Raw file inspection.

Loads the raw export as-downloaded and prints the shape and key
distributions so the scope filter in phase1b can be defined and
justified from what's actually in the file, not assumed.

Run from the analysis/ directory: python phase1_verify.py
"""
import pandas as pd

df = pd.read_csv('../data/raw_311_export.csv', dtype=str)

print("=== RAW FILE ===")
print("Total rows:", len(df))
print("Unique Unique Key:", df['Unique Key'].nunique())
print("Duplicate Unique Keys:", len(df) - df['Unique Key'].nunique())

df['Created Date'] = pd.to_datetime(df['Created Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Closed Date'] = pd.to_datetime(df['Closed Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

print("\nMin Created Date:", df['Created Date'].min())
print("Max Created Date:", df['Created Date'].max())

print("\nAgency values:\n", df['Agency'].value_counts())
print("\nBorough values:\n", df['Borough'].value_counts())
print("\nProblem values:\n", df['Problem (formerly Complaint Type)'].value_counts())
print("\nProblem Detail values:\n", df['Problem Detail (formerly Descriptor)'].value_counts())
print("\nStatus values:\n", df['Status'].value_counts())
