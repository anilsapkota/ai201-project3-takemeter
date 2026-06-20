import csv
from collections import Counter

with open("dataengineering_posts.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    posts = list(reader)

labeled = [p for p in posts if p["label"]]
labels = [p["label"] for p in labeled]

print(f"Total labeled: {len(labeled)}")
print("\n--- Label distribution ---")
for label, count in Counter(labels).items():
    pct = count / len(labeled) * 100
    print(f"{label}: {count} ({pct:.1f}%)")