import requests
from datetime import datetime

readme_file.close()
with open("README.md", "r+", encoding="utf‑8") as f:
    content = f.read()

ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
if ids:
    first_id = ids[0]
    item = requests.get(
        f"https://hacker-news.firebaseio.com/v0/item/{first_id}.json"
    ).json()
    title = item.get("title", "—")
else:
    title = "—"

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
new_block = f"\n\n**Latest HackerNews story:** {title}\n\n_Last updated: {now}_\n\n"

marker = "<!--hn-readme-->"

if marker in content:
    updated = content.split(marker)[0] + marker + new_block
else:
    updated = content + "\n" + marker + new_block

with open("README.md", "w", encoding="utf‑8") as f:
    f.write(updated)
