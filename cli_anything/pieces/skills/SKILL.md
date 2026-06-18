---
name: "cli-anything-pieces"
description: "CLI harness for Pieces OS — persistent long-term memory for AI agents and developers. Search assets, create memories, browse models, and inspect activities through the Pieces OS REST API (http://localhost:39300)."
version: "1.0.0"
category: "productivity"
tags:
  - pieces
  - memory
  - snippets
  - clipboard
  - llm
  - knowledge-management
  - cli
commands:
  - name: status
    description: Check Pieces OS connectivity, system info, API reachability, and asset count
    options: []
  - name: list
    description: List memory assets with optional type filter (snippet, image, file, etc.)
    options: ["--type", "--limit", "--offset"]
  - name: search
    description: Full-text search across memory assets
    options: ["--query", "--limit"]
  - name: create
    description: Create a new memory asset from text with optional tag/link annotations
    options: ["--text", "--name"]
  - name: models
    description: List available AI models known to Pieces OS
    options: []
  - name: activities
    description: Show recent activities (copy, save, link, etc.) with timestamps
    options: ["--limit"]
  - name: users
    description: List connected users and applications
    options: []
  - name: summaries
    description: Show recent workstream summaries (AI-generated context snapshots)
    options: ["--limit"]
---
