# Pieces OS CLI Harness

CLI harness to interact with **Pieces OS** — a local-first long-term
memory layer for developers.

## Prerequisites

- Pieces OS running on `http://localhost:39300`
- Python 3.10+

## Commands

| Command | Description |
|---------|-------------|
| `cli-anything-pieces status` | Check Pieces OS connectivity |
| `cli-anything-pieces list` | List saved memory assets |
| `cli-anything-pieces search <query>` | Search assets |
| `cli-anything-pieces create <text>` | Create a new asset |
| `cli-anything-pieces models` | List available AI models |
| `cli-anything-pieces models --provider open_ai` | Filter models by provider |
| `cli-anything-pieces info` | Show user profile |
| `cli-anything-pieces activities` | Show activity timeline |
| `cli-anything-pieces insights` | Show workstream summaries |
| `cli-anything-pieces conversations` | List copilot conversations |
| `cli-anything-pieces tags` | List all tags |
| `cli-anything-pieces get <asset_id>` | Show asset details |

Append `--json` to any command for raw JSON output.
