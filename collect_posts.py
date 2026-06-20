import requests
import csv
import time

headers = {"User-Agent": "takemeter-data-collector"}

collected_posts = []
seen_texts = set()

print("Collecting posts from Arctic Shift archive...")

# pull from different time windows to get more variety
time_filters = [
    "",                      # no filter
    "&after=2024-01-01",    # posts after Jan 2024
    "&after=2023-01-01&before=2024-01-01",  # all of 2023
    "&after=2022-01-01&before=2023-01-01",  # all of 2022
    "&after=2021-01-01&before=2022-01-01",  # all of 2021
]

for time_filter in time_filters:
    url = f"https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=dataengineering&limit=100&sort=desc{time_filter}"
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code} | Filter: '{time_filter or 'none'}'")
    
    if response.status_code != 200:
        print("Error:", response.text[:200])
        continue
    
    data = response.json()
    posts = data.get("data", [])
    
    new_this_batch = 0
    for post in posts:
        title = post.get("title", "")
        body = post.get("selftext", "")
        flair = post.get("link_flair_text", "")
        
        if body in ["[removed]", "[deleted]"]:
            body = ""
        
        full_text = (title + " " + body).strip()
        
        if len(full_text) < 20:
            continue
        
        # deduplicate on the fly
        key = full_text[:100]
        if key in seen_texts:
            continue
        
        seen_texts.add(key)
        collected_posts.append({
            "text": full_text,
            "flair": flair,
            "label": "",
            "notes": ""
        })
        new_this_batch += 1
    
    print(f"  {new_this_batch} new posts | Total: {len(collected_posts)}")
    time.sleep(2)

# save to CSV
with open("dataengineering_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "flair", "label", "notes"])
    writer.writeheader()
    writer.writerows(collected_posts)

print(f"\nDone! Saved {len(collected_posts)} unique posts to dataengineering_posts.csv")