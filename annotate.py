import csv

# load posts
with open("dataengineering_posts.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    posts = list(reader)

# find first unlabeled post
start = 0
for i, post in enumerate(posts):
    if not post["label"]:
        start = i
        break

labeled = sum(1 for p in posts if p["label"])
print(f"Progress: {labeled}/{len(posts)} labeled")
print(f"Starting at post {start + 1}")
print("\nLabels: c=career | t=technical | o=opinion | s=showcase | skip=skip")
print("Type 'quit' to save and exit\n")

for i in range(start, len(posts)):
    post = posts[i]
    
    # show the post
    print(f"\n{'='*60}")
    print(f"Post {i+1}/{len(posts)} | Flair: {post['flair']}")
    print(f"{'='*60}")
    print(post["text"][:400])
    if len(post["text"]) > 400:
        print("... [truncated]")
    print()
    
    # get label
    while True:
        choice = input("Label (c/t/o/s/skip/quit): ").strip().lower()
        
        if choice == "quit":
            break
        elif choice == "c":
            posts[i]["label"] = "career"
            break
        elif choice == "t":
            posts[i]["label"] = "technical"
            break
        elif choice == "o":
            posts[i]["label"] = "opinion"
            break
        elif choice == "s":
            posts[i]["label"] = "showcase"
            break
        elif choice == "skip":
            break
        else:
            print("Invalid. Use c, t, o, s, skip, or quit")
    
    if choice == "quit":
        break
    
    # save after every 10 posts
    if (i + 1) % 10 == 0:
        with open("dataengineering_posts.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "flair", "label", "notes"])
            writer.writeheader()
            writer.writerows(posts)
        labeled = sum(1 for p in posts if p["label"])
        print(f"\n✓ Auto-saved! Progress: {labeled} labeled so far\n")

# final save
with open("dataengineering_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "flair", "label", "notes"])
    writer.writeheader()
    writer.writerows(posts)

labeled = sum(1 for p in posts if p["label"])
print(f"\nSaved! Total labeled: {labeled}/{len(posts)}")