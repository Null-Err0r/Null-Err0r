import requests
from datetime import datetime
from time import sleep

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
top_ids = ids[:10]

entries = []
for id in top_ids:
    item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
    title = item.get("title", "📰")
    url = item.get("url", f"https://news.ycombinator.com/item?id={id}")
    time_utc = datetime.utcfromtimestamp(item.get("time", 0)).strftime('%Y-%m-%d %H:%M UTC')
    entries.append(f"🔹 [{title}]({url}) — `{time_utc}`")
    sleep(0.3)

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
entry_block = "\n".join(entries)
new_block = f"""
### 📰 Hacker News (Every 15 minutes)

{entry_block}

_latest update: {now}_

"""

marker = "<!--hn-readme-->"
if marker in content:
    updated = content.split(marker)[0] + marker + "\n" + new_block
else:
    updated = content + "\n" + marker + "\n" + new_block

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
