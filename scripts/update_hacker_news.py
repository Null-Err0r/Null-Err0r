
import requests
import re
from datetime import datetime
import pytz

MAX_STORIES = 10
HN_API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_API_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"
README_FILE = "README.md"

def get_top_stories():
    try:
        response = requests.get(HN_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching top stories: {e}")
        return []

def get_story_details(story_id):
    try:
        url = ITEM_API_URL_TEMPLATE.format(story_id)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def format_story(story):
    title = story.get('title', 'N/A')
    url = story.get('url', '#')
    timestamp = story.get('time', 0)
    story_time_utc = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    time_str = story_time_utc.strftime('%Y-%m-%d %H:%M UTC')

    # Format with a line break and indented date
    return (
        f"🔹 <a href='{url}' target='_blank' rel='noopener noreferrer'>{title}</a><br>\n"
        f"&nbsp;&nbsp;&nbsp;&nbsp;— <small>{time_str}</small>"
    )

def update_readme(content, timestamp):
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_text = f.read()

        # Replace news content
        news_placeholder = r"<!-- HACKER_NEWS_START -->(.|\n)*<!-- HACKER_NEWS_END -->"
        news_replacement = f"<!-- HACKER_NEWS_START -->\n{content}\n<!-- HACKER_NEWS_END -->"
        new_readme, count = re.subn(news_placeholder, replacement, readme_text)

        if count == 0:
            print("Warning: HACKER_NEWS_START placeholder not found.")
            return

        # Replace last updated timestamp
        timestamp_placeholder = r"<!-- HACKER_NEWS_LAST_UPDATED -->(.|\n)*<!-- /HACKER_NEWS_LAST_UPDATED -->"
        timestamp_replacement = f"<!-- HACKER_NEWS_LAST_UPDATED -->{timestamp}<!-- /HACKER_NEWS_LAST_UPDATED -->"
        new_readme, _ = re.subn(timestamp_placeholder, timestamp_replacement, new_readme)

        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_readme)
        
        print("README updated successfully with Hacker News stories.")

    except FileNotFoundError:
        print(f"Error: {README_FILE} not found.")

if __name__ == "__main__":
    story_ids = get_top_stories()
    if story_ids:
        stories_markdown = [format_story(get_story_details(sid)) for sid in story_ids[:MAX_STORIES] if get_story_details(sid)]
        update_time = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        update_readme("\n".join(stories_markdown), update_time)
