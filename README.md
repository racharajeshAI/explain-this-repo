# Explain This Repo to My Mom

Paste a GitHub repo URL. Get a plain-English explanation anyone can understand.

No jargon. No code talk. Just "here's what this thing does."

## Just use the website

Go to [the site](https://racharajeshai.github.io/explain-this-repo/), paste a URL, done. No install, no setup, nothing to download.

Want better explanations? You can connect a local AI model -- see below.

## Want AI-powered explanations?

You can run a local AI model on your computer for way better results. One-time setup -- just ask your son to do this, takes 5 minutes.

**Step 1** -- Download Ollama
- Go to [ollama.com](https://ollama.com) and grab the installer
- Or if your son knows homebrew: `brew install ollama`

**Step 2** -- Open Terminal and pull a model
```bash
ollama pull llama3
```
Your son might suggest a different model, that's fine, any of them work.

**Step 3** -- Make sure Ollama is running
```bash
ollama serve
```
If it says "address already in use" -- that's fine, it's already running.

**Step 4** -- Go back to [the website](https://racharajeshai.github.io/explain-this-repo/), click Settings, toggle "Use Local LLM", hit "Scan for models", pick one. Done.

## CLI (just in case)

For terminal people. Also a one-time thing -- ask your son, 30 seconds.

```bash
git clone https://github.com/racharajeshAI/explain-this-repo.git
cd explain-this-repo
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
```

Then:
```bash
python main.py https://github.com/fastapi/fastapi
python main.py facebook/react  # short format works too
```

## How It Works

1. You give it a GitHub URL
2. It grabs the repo's README, description, and file structure
3. AI reads all that and explains it like you're talking to a friend
4. Saves the explanation as a markdown file

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key (CLI only) |
| `GITHUB_TOKEN` | No | GitHub token to avoid rate limits |
