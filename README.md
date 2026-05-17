# Explain This Repo to My Mom

Paste a GitHub repo URL. Get a plain-English explanation anyone can understand.

No jargon. No code talk. Just "here's what this thing does."

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
```

## Usage

```bash
python main.py https://github.com/fastapi/fastapi
python main.py https://github.com/facebook/react
python main.py facebook/react  # short format works too
```

## Output

```
============================================================
  EXPLAINING: fastapi/fastapi
============================================================

Imagine you're ordering food at a restaurant. You tell the waiter
what you want, the kitchen makes it, and it arrives at your table
hot and correct. FastAPI is like that waiter for apps on your phone
or website...

============================================================

Saved to: fastapi_explained.md
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `GITHUB_TOKEN` | No | GitHub token to avoid rate limits |

## How It Works

1. You give it a GitHub URL
2. It grabs the repo's README, description, and file structure
3. AI reads all that and explains it like you're talking to a friend
4. Saves the explanation as a markdown file
