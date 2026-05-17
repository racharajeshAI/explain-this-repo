#!/usr/bin/env python3
"""
Explain This Repo to My Mom
---------------------------
Paste a GitHub repo URL. Get a plain-English explanation.
No jargon. No code snippets. Just "here's what this thing does."
"""

import sys
import os
import re
import requests
from openai import OpenAI

GITHUB_API = "https://api.github.com"


def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract owner/repo from various GitHub URL formats."""
    url = url.strip().rstrip("/")

    # Handle: github.com/owner/repo
    # Handle: https://github.com/owner/repo
    # Handle: github.com/owner/repo.git
    patterns = [
        r"github\.com/([^/]+)/([^/\.]+)",
        r"^([^/]+)/([^/\.]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)

    raise ValueError(f"Can't parse this as a GitHub repo: {url}")


def fetch_repo_info(owner: str, repo: str, token: str = None) -> dict:
    """Grab repo metadata from GitHub API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}", headers=headers)
    resp.raise_for_status()
    return resp.json()


def fetch_readme(owner: str, repo: str, token: str = None) -> str:
    """Fetch the README content."""
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/readme", headers=headers
    )
    if resp.status_code == 404:
        return "(No README found)"
    resp.raise_for_status()
    return resp.text[:8000]  # Cap at 8k chars to save tokens


def fetch_file_tree(owner: str, repo: str, token: str = None) -> str:
    """Get the top-level file/folder structure."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/contents", headers=headers
    )
    if resp.status_code != 200:
        return "(Could not fetch file tree)"

    items = resp.json()
    lines = []
    for item in sorted(items, key=lambda x: (x["type"] != "dir", x["name"])):
        prefix = "📁 " if item["type"] == "dir" else "📄 "
        lines.append(f"{prefix}{item['name']}")
    return "\n".join(lines)


def explain_repo(repo_info: dict, readme: str, file_tree: str) -> str:
    """Use AI to generate a plain-English explanation."""
    client = OpenAI()  # Uses OPENAI_API_KEY from env

    prompt = f"""You are explaining a GitHub repository to someone who has NEVER written a line of code.
Think: a parent, a friend at dinner, someone curious but non-technical.

RULES:
- NO jargon (no "API", "framework", "library", "repo", "backend", "frontend")
- Use everyday analogies and comparisons
- Keep it under 300 words
- Explain like you're telling a story, not reading a spec
- Mention what problem it solves for regular people
- If it's a developer tool, explain what it helps people BUILD or DO, not how it works

REPO INFO:
- Name: {repo_info.get('name', 'Unknown')}
- Description: {repo_info.get('description', 'No description provided')}
- Stars: {repo_info.get('stargazers_count', 0)}
- Language: {repo_info.get('language', 'Unknown')}
- Topics: {', '.join(repo_info.get('topics', []))}

FILE STRUCTURE:
{file_tree}

README (excerpt):
{readme[:4000]}

Write the explanation now. Start with a one-sentence summary, then expand."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <github-repo-url>")
        print("Example: python main.py https://github.com/fastapi/fastapi")
        sys.exit(1)

    url = sys.argv[1]
    github_token = os.environ.get("GITHUB_TOKEN")  # Optional, avoids rate limits

    try:
        owner, repo = parse_repo_url(url)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Looking up {owner}/{repo}...")

    try:
        repo_info = fetch_repo_info(owner, repo, github_token)
        readme = fetch_readme(owner, repo, github_token)
        file_tree = fetch_file_tree(owner, repo, github_token)
    except requests.exceptions.HTTPError as e:
        print(f"GitHub API error: {e}")
        sys.exit(1)

    print(f"Found: {repo_info.get('description', 'No description')}")
    print(f"Stars: {repo_info.get('stargazers_count', 0)}")
    print(f"\nGenerating explanation...\n")

    explanation = explain_repo(repo_info, readme, file_tree)

    print("=" * 60)
    print(f"  EXPLAINING: {owner}/{repo}")
    print("=" * 60)
    print()
    print(explanation)
    print()
    print("=" * 60)

    # Save to file
    output_file = f"{repo}_explained.md"
    with open(output_file, "w") as f:
        f.write(f"# {owner}/{repo} — Explained Simply\n\n")
        f.write(explanation)
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
