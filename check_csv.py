import csv

with open("dataengineering_posts.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    posts = list(reader)

print(f"Total posts: {len(posts)}")
print(f"Columns: {posts[0].keys()}")
print("\n--- First 3 posts ---")
for post in posts[:3]:
    print("TEXT:", post["text"][:150])
    print("FLAIR:", post["flair"])
    print("LABEL:", post["label"])
    print("---")