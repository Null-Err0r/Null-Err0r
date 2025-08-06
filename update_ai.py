
import re
import json
import sys

def update_readme():
    """
    Reads a JSON of GitHub issues from stdin, formats them,
    and updates the README.md file between specified markers.
    """
    try:
        issues_json = sys.stdin.read()
        if not issues_json:
            print("No input received from stdin.")
            return
        issues = json.loads(issues_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input.")
        sys.exit(1)

    # Build the markdown list of conversations
    conversation_list = []
    for issue in issues:
        title = issue.get('title', 'No Title').replace('[', '\\[').replace(']', '\\]')
        url = issue.get('url', '#')
        conversation_list.append(f"* [{title}]({url})")

    if not conversation_list:
        conversations_md = "No recent conversations."
    else:
        conversations_md = "\n".join(conversation_list)

    # Read the current README content
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print("Error: README.md not found.")
        sys.exit(1)

    # Use regex to replace the content between the markers
    # re.DOTALL allows '.' to match newlines
    placeholder_pattern = r"<!-- CHAT_LOG_START -->(.|\n)*<!-- CHAT_LOG_END -->"
    replacement_text = f"<!-- CHAT_LOG_START -->\n{conversations_md}\n<!-- CHAT_LOG_END -->"
    
    new_readme, num_replacements = re.subn(placeholder_pattern, replacement_text, readme_content)

    if num_replacements == 0:
        print("Warning: Placeholder '<!-- CHAT_LOG_START -->' not found in README.md.")
        return

    # Write the updated content back to the README.md file
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md updated successfully with recent conversations.")

if __name__ == "__main__":
    update_readme()
