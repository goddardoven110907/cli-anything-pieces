# Pieces OS CLI Harness

`cli-anything-pieces` — Agent-native CLI for [Pieces OS](https://pieces.app), the persistent long-term memory layer for developers and AI agents.

Manage memory assets, search snippets, browse models, and inspect activities via the Pieces OS REST API.

## Requirements

- **Pieces OS** running locally (default: `http://localhost:39300`)
- Python ≥ 3.10

## Install

```bash
pip install git+https://github.com/goddardenoven110907/cli-anything-pieces.git
```

## Commands

| Command      | Description                                       |
| ------------ | ------------------------------------------------- |
| `status`     | Check Pieces OS connectivity and system info      |
| `list`       | List memory assets (optionally by type)            |
| `search`     | Full-text search across memory assets              |
| `create`     | Create a new memory asset from text                |
| `models`     | List available AI models                           |
| `activities` | Show recent activities with timestamps             |
| `users`      | List connected users and applications              |
| `summaries`  | Show recent workstream summaries                   |

### Usage

```bash
cli-anything-pieces status
cli-anything-pieces list --limit 20
cli-anything-pieces search --query "docker networking"
cli-anything-pieces create --text "Important note about deployment"
cli-anything-pieces activities --limit 10
```

## Environment

| Variable         | Default                          | Description              |
| ---------------- | -------------------------------- | ------------------------ |
| `PIECES_API_BASE` | `http://localhost:39300`        | Pieces OS API base URL   |
| `PIECES_APP_ID`   | Auto-generated UUID             | Application identifier   |

## Category

Productivity / Knowledge Management
