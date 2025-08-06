import requests
import re
import os
import sys
from datetime import datetime
import pytz

MAX_STORIES = 10
HN_API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_API_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"
README_PATH = os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "README.md")

def get_story_details(story_id):
    try:
        response = requests.get(ITEM_API_URL_TEMPLATE.format(story_id))
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def format_story(story):

    title = story.get('title', 'N/A')
    url = story.get('url', '#')
    timestamp = story.get('time', 0)
    time_str = datetime.fromtimestamp(timestamp, tz=pytz.utc).strftime('%Y-%m-%d %H:%M UTC')
        return f"🔹 <a href='{url}' target='_blank' rel='noopener noreferrer'>{title}</a><br><sub>&nbsp;&nbsp;&nbsp;&nbsp;— {time_str}</sub>"

def main():
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: README.md not found at path: {README_PATH}")
        sys.exit(1) 

    try:
        story_ids = requests.get(HN_API_URL).json()
    except Exception as e:
        print(f"Error fetching story IDs: {e}")
        return

    stories_markdown = [format_story(details) for sid in story_ids[:MAX_STORIES] if (details := get_story_details(sid))]
    
    if not stories_markdown:
        print("No stories fetched, not updating README.")
        return

    content = "<br><br>\n".join(stories_markdown)

    news_placeholder = r"(.|\n)*"
    news_replacement = f"\n{content}\n"
    new_readme, count = re.subn(news_placeholder, news_replacement, readme_content)
    
    if count == 0:
        print("Warning: HACKER_NEWS_START placeholder not found in README.md.")
        return
        
    update_time = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    timestamp_placeholder = r"(.|\n)*"
    timestamp_replacement = f"\nLast Updated: {update_time}\n"
    new_readme = re.sub(timestamp_placeholder, timestamp_replacement, new_readme)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)
    
    print("README.md updated successfully with Hacker News stories.")

if __name__ == "__main__":
    main()
