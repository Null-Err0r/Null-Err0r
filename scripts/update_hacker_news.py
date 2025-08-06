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

NEWS_PLACEHOLDER = r"(.|\n)*"
TIMESTAMP_PLACEHOLDER = r"(.|\n)*"


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
    """تابع اصلی برای خواندن، به‌روزرسانی و نوشتن فایل README."""
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"CRITICAL ERROR: README.md not found at path: {README_PATH}")
        sys.exit(1)

    try:
        story_ids = requests.get(HN_API_URL).json()
    except Exception as e:
        print(f"Error fetching story IDs: {e}")
        return 

    stories = [details for sid in story_ids[:MAX_STORIES] if (details := get_story_details(sid))]
    
    if not stories:
        print("No stories fetched, not updating README.")
        return

    stories_markdown = [format_story(s) for s in stories]
    news_content = "<br><br>\n".join(stories_markdown)
    
    new_readme, news_update_count = re.subn(
        NEWS_PLACEHOLDER,
        f"\n{news_content}\n",
        readme_content
    )
    
    if news_update_count == 0:
        print("CRITICAL ERROR: HACKER_NEWS_START placeholder not found in README.md.")
        sys.exit(1)

    update_time = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    new_readme, timestamp_update_count = re.subn(
        TIMESTAMP_PLACEHOLDER,
        f"{update_time}",
        new_readme 
    )

    if timestamp_update_count == 0:
        print("WARNING: HACKER_NEWS_LAST_UPDATED placeholder not found. Skipping timestamp update.")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)
    
    print("README.md updated successfully.")


if __name__ == "__main__":
    main()
