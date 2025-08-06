import re
import json
import sys

def update_readme():
    readme_path = "README.md"
    
    try:
        issues_json = sys.stdin.read()
        if not issues_json:
            print("No input received from stdin for chat log.")
            return
        issues = json.loads(issues_json)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON input for chat log. Received: {issues_json}")
        sys.exit(1)

    conversation_list = [f"* [{issue.get('title', 'No Title').replace('[', '\\[').replace(']', '\\]')}]({issue.get('url', '#')})" for issue in issues]
    
    if not conversation_list:
        conversations_md = "No recent conversations."
    else:
        conversations_md = "\n".join(conversation_list)

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found.")
        sys.exit(1)

    placeholder_pattern = r"<!-- CHAT_LOG_START -->(.|\n)*<!-- CHAT_LOG_END -->"
    replacement_text = f"<!-- CHAT_LOG_START -->\n{conversations_md}\n<!-- CHAT_LOG_END -->"
    
    new_readme, num_replacements = re.subn(placeholder_pattern, replacement_text, readme_content)

    if num_replacements == 0:
        print("Warning: Placeholder '<!-- CHAT_LOG_START -->' not found in README.md.")
        return

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md updated successfully with recent conversations.")

if __name__ == "__main__":
    update_readme()
