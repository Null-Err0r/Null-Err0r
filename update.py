import requests
from datetime import datetime
from time import sleep

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
top_ids = ids[:10]

entries = []
for i, id in enumerate(top_ids, start=1):
    item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
    title = item.get("title", "بدون عنوان")
    url = item.get("url", f"https://news.ycombinator.com/item?id={id}")
    time_utc = datetime.utcfromtimestamp(item.get("time", 0)).strftime('%Y-%m-%d %H:%M')
    entries.append(f"🔹 [{title}]({url}) <sub><sup>({time_utc} UTC)</sup></sub>")
    sleep(0.3) 

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
entry_block = "\n".join(entries)
new_block = f"""
<div align="center">

### 📰 Hacker News ( Every 15 minutes )

{entry_block}

<sub><sup>latest: {now}</sup></sub>

</div>
"""

marker = "<!--hn-readme-->"
if marker in content:
    updated = content.split(marker)[0] + marker + new_block
else:
    updated = content + "\n" + marker + new_block

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
