# mini-sidekick

Proof of concept for an agent-based personal finance tool.

**In scope:** LangGraph agent (Planner → Extractor → Executor), EasyOCR on receipt images, Claude API for structured extraction, SQLite with a single `transactions` table, duplicate detection in the Planner, CLI entrypoint and history viewer.

**Out of scope (v2):** Gradio UI, auth, vendor/category tables, web enrichment, Docker, Postgres, local LLM.

## Quick setup

git clone <repo-url>
cd mini-sidekick

uv sync
cp .env.example .env   # then fill in
uv run python -m main

## Working a story

```bash
# 1. Sync main
git checkout main
git pull

# 2. Branch, named after the story ID
git checkout -b "feature"

# 3. Work; commit in small logical chunks
git add -A
git commit -m "commit message"

# 4. Push and open a PR
git push

# 5. After PR is merged, clean up locally
git checkout main
git pull
git branch -d "feature"
```