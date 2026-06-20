import csv

# load your labeled posts
with open("dataengineering_posts.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    posts = list(reader)

# find examples of each error type we saw in confusion matrix
print("=== OPINION posts (model confused with career) ===")
opinion_posts = [p for p in posts if p["label"] == "opinion"]
for p in opinion_posts[:5]:
    print(p["text"][:200])
    print("---")

print("\n=== TECHNICAL posts (model confused with career) ===")
technical_posts = [p for p in posts if p["label"] == "technical"]
for p in technical_posts[:5]:
    print(p["text"][:200])
    print("---")

print("\n=== SHOWCASE posts (model confused with technical) ===")
showcase_posts = [p for p in posts if p["label"] == "showcase"]
for p in showcase_posts[:5]:
    print(p["text"][:200])
    print("---")