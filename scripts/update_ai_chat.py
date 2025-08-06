import re
import json
import sys
import os

# Define absolute paths for reliability
WORKSPACE = os.environ.get("GITHUB_WORKSPACE", ".")
README_PATH = os.path.join(WORKSPACE, "README.md")
ISSUES_FILE_PATH = os.path.join(WORKSPACE, "issues.json")

def main():
    # Read issues from the temporary file instead of stdin
    try:
        with open(ISSUES_FILE_PATH, "r", encoding="utf-8") as f:
            issues = json.load(f)
    except FileNotFoundError:
        print(f"Error: issues.json not found at {ISSUES_FILE_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {ISSUES_FILE_PATH}")
        sys.exit(1)

    # Read the current README content
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: README.md not found at {README_PATH}")
        sys.exit(1)

    # Format conversations
    conversation_list = [f"* [{issue.get('title', 'No Title').replace('[', '\\[').replace(']', '\\]')}]({issue.get('url', '#')})" for issue in issues]
    conversations_md = "\n".join(conversation_list) if conversation_list else "No recent conversations."

    # Replace chat log content in README
    placeholder_pattern = r"<!-- CHAT_LOG_START -->(.|\n)*<!-- CHAT_LOG_END -->"
    new_readme, num_replacements = re.subn(
        placeholder_pattern,
        f"<!-- CHAT_LOG_START -->\n{conversations_md}\n<!-- CHAT_LOG_END -->",
        readme_content
    )

    if num_replacements == 0:
        print("Warning: Placeholder '<!-- CHAT_LOG_START -->' not found in README.md.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md updated successfully with recent conversations.")

if __name__ == "__main__":
    main()
