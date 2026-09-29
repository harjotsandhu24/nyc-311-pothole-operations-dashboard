"""
Phase 4 — Monthly volume and ZIP-level aggregation.

Produces the numbers behind the dashboard's monthly volume chart and
the closed-rate figure. ZIP breakdowns explicitly exclude the records
missing an Incident Zip rather than silently dropping them from the
overall totals.

Run from the analysis/ directory: python phase4_monthly_zip.py
"""
import pandas as pd

scoped = pd.read_csv('../data/scoped_2025_brooklyn_pothole.csv', dtype=str)
scoped['Created Date'] = pd.to_datetime(scoped['Created Date'])

monthly = scoped.groupby(scoped['Created Date'].dt.month).size()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print("=== Monthly volume ===")
for i, count in monthly.items():
    print(month_names[i - 1], count)
print("\nHighest month:", month_names[monthly.idxmax() - 1], monthly.max())
print("Lowest month:", month_names[monthly.idxmin() - 1], monthly.min())

print("\n=== ZIP distribution ===")
zip_counts = scoped['Incident Zip'].value_counts(dropna=False)
print("Number of distinct ZIPs (excl. missing):", scoped['Incident Zip'].dropna().nunique())
print("Missing ZIP:", scoped['Incident Zip'].isna().sum())
print("\nTop 10 ZIPs:")
print(zip_counts.head(10))
print("\nMedian requests per ZIP:", scoped['Incident Zip'].dropna().value_counts().median())
print("Min requests per ZIP:", scoped['Incident Zip'].dropna().value_counts().min())

# closed %
status_counts = scoped['Status'].value_counts()
closed_pct = status_counts['Closed'] / len(scoped) * 100
print(f"\nClosed %: {closed_pct:.1f}%")
print(status_counts)
