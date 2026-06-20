import requests
import csv
import time

headers = {"User-Agent": "takemeter-data-collector"}

collected_posts = []
after = None

print("Collecting posts from Arctic Shift archive...")

for page in range(5):
    
    url = "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=dataengineering&limit=100&sort=desc"
    if after:
        url += f"&after={after}"
    
    response = requests.get(url, headers=headers)
    print(f"Page {page + 1} status code: {response.status_code}")
    
    if response.status_code != 200:
        print("Error:", response.text[:300])
        break
    
    data = response.json()
    posts = data.get("data", [])
    
    if not posts:
        print("No more posts found.")
        break
    
    for post in posts:
        title = post.get("title", "")
        body = post.get("selftext", "")
        flair = post.get("link_flair_text", "")
        
        if body in ["[removed]", "[deleted]"]:
            body = ""
        
        full_text = (title + " " + body).strip()
        
        if len(full_text) < 20:
            continue
        
        collected_posts.append({
            "text": full_text,
            "flair": flair,
            "label": "",
            "notes": ""
        })
    
    # use the created_utc of the last post as the "after" cursor
    after = posts[-1].get("created_utc")
    
    print(f"  Collected {len(collected_posts)} posts so far...")
    time.sleep(2)

with open("dataengineering_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "flair", "label", "notes"])
    writer.writeheader()
    writer.writerows(collected_posts)

print(f"\nDone! Saved {len(collected_posts)} posts to dataengineering_posts.csv")