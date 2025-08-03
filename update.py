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
    entries.append(
        f'  <li>🔹 <a href="{url}" style="color: #f7931a; text-decoration: none;">{title}</a> — <code>{time_utc}</code></li>'
    )
    sleep(0.3)

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
entry_block = "\n".join(entries)

new_block = f"""
<!--hn-readme-->
<div align="center" style="border: 1px solid #f7931a; border-radius: 10px; padding: 20px; max-width: 700px; margin: auto; background-color: #1d2021; color: #f7931a; font-family: 'Fira Code', monospace;">

<h3>📰 Hacker News (Every 15 minutes)</h3>

<ul style="list-style-type: none; padding-left: 0; line-height: 1.6;">
{entry_block}
</ul>

<p style="font-size: 0.8em; color: #aaaaaa; margin-top: 10px;">
  latest update: {now}
</p>

</div>
<!--hn-readme-->
"""

marker = "<!--hn-readme-->"
if marker in content:
    updated = content.split(marker)[0] + new_block + content.split(marker)[2] if len(content.split(marker)) > 2 else content.split(marker)[0] + new_block
else:
    updated = content + "\n" + new_block

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
