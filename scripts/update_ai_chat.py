import re
import json
import sys
import os

WORKSPACE = os.environ.get("GITHUB_WORKSPACE", ".")
README_PATH = os.path.join(WORKSPACE, "README.md")
ISSUES_FILE_PATH = os.path.join(WORKSPACE, "issues.json")

def main():
    try:
        with open(ISSUES_FILE_PATH, "r", encoding="utf-8") as f:
            issues = json.load(f)
    except Exception as e:
        print(f"Error loading issues.json: {e}")
        sys.exit(1)

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"README.md not found at {README_PATH}")
        sys.exit(1)

    conversation_list = []
    for issue in issues:
        title = issue.get('title', 'No Title')
        url = issue.get('url', '#')
        response = issue.get('last_comment', '').strip().replace('\n', ' ')
        if len(response) > 300:
            response = response[:300] + "..."
        line = f"* [{title}]({url})  \n  <sub>{response}</sub>"
        conversation_list.append(line)

    conversations_md = "\n\n".join(conversation_list) if conversation_list else "No recent conversations."

    new_readme, replaced = re.subn(
        r"<!-- CHAT_LOG_START -->(.|\n)*<!-- CHAT_LOG_END -->",
        f"<!-- CHAT_LOG_START -->\n{conversations_md}\n<!-- CHAT_LOG_END -->",
        readme_content
    )

    if replaced == 0:
        print("Warning: CHAT_LOG_START placeholder not found in README.md.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README updated with recent conversations.")

if __name__ == "__main__":
    main()
