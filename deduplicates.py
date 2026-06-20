import csv

with open("dataengineering_posts.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# deduplicate by text
seen = set()
unique_rows = []
for row in rows:
    key = row["text"][:100]  # first 100 chars as unique key
    if key not in seen:
        seen.add(key)
        unique_rows.append(row)

with open("dataengineering_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "flair", "label", "notes"])
    writer.writeheader()
    writer.writerows(unique_rows)

print(f"Before: {len(rows)} rows")
print(f"After deduplication: {len(unique_rows)} rows")