# agent-from-scratch

An AI agent built from scratch — my own loop, tools, and safety gates,
no frameworks, runs on a local model.

## Why

I'm building this to learn how AI agents actually work — how they use
tools, call MCP servers, read and write files, and write code. Not by
reading about it: by building every piece myself and understanding
every line. The commit history is my learning diary.

## What it does today

Right now it's a chatbot that talks as my personal assistant, streaming
its answers live as the model thinks. Small, but every line of it is
mine and readable — the whole program is explained in plain English
comments, top to bottom.

The long game: piece by piece, this agent takes over what Claude Code
does for me today.

## Run it

You need [Ollama](https://ollama.com) running with a model that does
chat. I use a customized Hermes 3; any chat model works:

```
ollama pull hermes3:8b
python3 agent.py
```

Then edit the `MODEL` line at the top of `agent.py` to name the model
you pulled. That one line is the whole "swappable brain" — the rest of
the code never knows which model is behind it.

## Roadmap

- **v1 — the loop** ✓ — chat with memory (the conversation list)
- **v1.1 — streaming** ✓ — watch the model think live
- **v2 — first tool** — `read_file`: the model asks, my code decides
- **v2.5 — the scoreboard** — ten real tasks from my life as a test
  suite; every harness upgrade gets measured, so I can watch the
  capability line move instead of guessing
- **v3 — the router** — too hard for the small model? It says so and
  escalates to a stronger brain
- **v4 — memory** — the agent starts learning between sessions
- **v5 — reasoning** — think first, act second, check the work
- **someday — my own brain** — a tiny GPT trained from zero, plugged
  into this same harness

## Tool wishlist (each one = the same pattern as v2)

- `search_web` — the model asks, my code hits a search API
- `fetch_page` — read a webpage it found
- `write_file` — it drafts, I approve before anything touches disk
- `run_command` — someday, behind a hard allowlist

Search + fetch together is the goal that matters: the agent stops being
a chatbot and starts being a researcher.

## House rules

1. Secrets never touch the code — that's why the `.gitignore` was the
   first commit.
2. Every file reads like a story: a plain-English map at the top,
   sections with banners, a memo on every move. If you can't read it,
   I broke a rule.
3. The model proposes; my code decides. The AI never runs anything my
   code didn't explicitly allow.
