import requests
import xml.etree.ElementTree as ET
import os

FEED_URL = "https://www.livelaw.in/category/sc-judgments/google_feeds.xml"
MD_FILE = "ll.md"

def fetch_and_update():
    response = requests.get(FEED_URL)
    if response.status_code != 200:
        print("Failed to fetch feed")
        return

    root = ET.fromstring(response.content)
    # The items are usually under <channel>
    items = root.findall(".//item")
    
    # Read existing content to avoid duplicates (optional but recommended)
    existing_content = ""
    if os.path.exists(MD_FILE):
        with open(MD_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()

    new_entries = []
    for item in items:
        title = item.find("title").text
        link = item.find("link").text
        pub_date = item.find("pubDate").text
        
        # Create a unique markdown entry
        entry = f"### [{title}]({link})\n*Published on: {pub_date}*\n\n"
        
        # Append if not already in the file
        if link not in existing_content:
            new_entries.append(entry)

    if new_entries:
        with open(MD_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(new_entries))
        print(f"Added {len(new_entries)} new cases.")
    else:
        print("No new cases found.")

if __name__ == "__main__":
    fetch_and_update()
