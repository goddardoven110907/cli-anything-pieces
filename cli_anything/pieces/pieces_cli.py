#!/usr/bin/env python3
"""Pieces OS CLI — manage long-term memory, search assets, browse models and activities.

Uses the Pieces OS REST API at http://localhost:39300.

Commands:
  status      Check Pieces OS connectivity and system info
  list        List memory assets
  search      Search assets by query
  create      Create a new memory asset from text
  models      List available AI models
  activities  Show recent activities
  users       List connected users/applications
  summaries   Show workstream summaries
"""

import json
import sys
import os
import textwrap
from urllib.request import Request, urlopen
from urllib.error import URLError

API_BASE = os.environ.get("PIECES_API_BASE", "http://localhost:39300")
APPLICATION_ID = os.environ.get(
    "PIECES_APP_ID",
    "af16ab12-f597-41a6-9165-768abba4434a"
)
PIECES_APP = {
    "id": APPLICATION_ID,
    "name": "PIECES_FOR_DEVELOPERS",
    "version": "6.0.1",
    "platform": "WINDOWS",
    "onboarded": True,
    "privacy": "OPEN",
}


def api(method: str, path: str, body: dict | None = None, timeout: int = 10):
    """Make a request to the Pieces OS API."""
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except URLError as e:
        print(f"  [error] {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("  [error] invalid JSON response", file=sys.stderr)
        return None


def _readable(d, default="?"):
    """Extract human-readable timestamp from a Pieces OS created/updated object."""
    if isinstance(d, dict):
        return d.get("readable", d.get("value", default))
    return str(d)


# ── commands ──────────────────────────────────────────────────────

def cmd_status():
    """Check Pieces OS connectivity and show brief system info."""
    data = api("GET", "/users")
    if data is None:
        print("  Status: OFFLINE  (Pieces OS not reachable)")
        return 1

    users = data.get("iterable", [])
    app_data = api("GET", "/applications")
    apps = []
    if app_data:
        apps = [a.get("name", "?") for a in app_data.get("iterable", [])]

    models_data = api("GET", "/models?limit=1")
    model_count = len(models_data.get("iterable", [])) if models_data else 0

    assets_data = api("GET", "/assets?limit=0")
    asset_count = len(assets_data.get("iterable", [])) if assets_data else 0

    print(f"  Pieces OS:    RUNNING")
    print(f"  Users:        {len(users)} connected")
    print(f"  Applications: {', '.join(apps) if apps else 'none'}")
    print(f"  Models:       {model_count} available")
    print(f"  Assets:       {asset_count} in memory")
    return 0


def cmd_list():
    """List memory assets (names and previews)."""
    data = api("GET", "/assets")
    if data is None:
        return 1

    items = data.get("iterable", [])
    if not items:
        print("  No assets found.")
        return 0

    for item in items:
        aid = item.get("id", "?")
        name = item.get("name", "Untitled")
        created = _readable(item.get("created", {}))
        # Try to get fragment text preview from formats
        formats = item.get("formats", {}).get("iterable", [])
        text_raw = ""
        for fmt in formats:
            ref = fmt.get("reference", fmt)
            frag = ref.get("fragment", {})
            text_raw = frag.get("string", {}).get("raw", "")
            if text_raw:
                break
        preview = text_raw[:60].replace("\n", " ") if text_raw else "(no text preview)"
        print(f"  [{aid[:8]}] {name}")
        print(f"        created: {created}  |  {preview}")
    print(f"\n  Total: {len(items)} assets")
    return 0


def cmd_search(query: str):
    """Search memory assets by query text."""
    body = {"query": query}
    data = api("POST", "/assets/search", body)
    if data is None:
        return 1

    results = data.get("results", {}).get("iterable", [])
    if not results:
        print(f"  No results for: {query}")
        return 0

    for item in results:
        asset = item.get("asset", {})
        aid = asset.get("id", "?")
        name = asset.get("name", "Untitled")
        # Get fragment text
        formats = asset.get("formats", {}).get("iterable", [])
        text_raw = ""
        for fmt in formats:
            ref = fmt.get("reference", fmt)
            frag = ref.get("fragment", {})
            text_raw = frag.get("string", {}).get("raw", "") or ""
            if text_raw:
                break
        if not text_raw:
            # Also check top-level fragment
            frag = asset.get("fragment", {})
            text_raw = frag.get("string", {}).get("raw", "")
        preview = text_raw[:80].replace("\n", " ") if text_raw else "(empty)"
        score = item.get("score", "?")
        print(f"  [{aid[:8]}] {name}  (score: {score})")
        print(f"        {preview}")
    print(f"\n  Results: {len(results)}")
    return 0


def cmd_create(text: str, name: str | None = None):
    """Create a new memory asset from text."""
    payload = {
        "asset": {
            "application": dict(PIECES_APP),
            "format": {
                "fragment": {
                    "string": {"raw": text}
                }
            },
        },
        "type": "SEEDED_ASSET",
    }
    data = api("POST", "/assets/create", payload)
    if data is None:
        return 1

    aid = data.get("id", "?")
    aname = data.get("name", "Untitled")
    print(f"  Created: [{aid[:8]}] {aname}")
    print(f"  Pieces OS is processing 'unknown material' - name may update.")
    return 0


def cmd_models():
    """List available AI models."""
    data = api("GET", "/models")
    if data is None:
        return 1

    models = data.get("iterable", [])
    if not models:
        print("  No models found.")
        return 0

    for m in models:
        mid = m.get("id", "?")[:12]
        name = m.get("name", "?")
        provider = m.get("provider", "?")
        m_type = m.get("type", "?")
        capabilities = ", ".join(m.get("capabilities", [])) if m.get("capabilities") else ""
        detail = f" ({capabilities})" if capabilities else ""
        print(f"  [{mid}] {name} ({provider}){detail}")
    print(f"\n  Total: {len(models)} models")
    return 0


def cmd_activities():
    """Show recent activities."""
    data = api("GET", "/activities?limit=10")
    if data is None:
        return 1

    items = data.get("iterable", [])
    if not items:
        print("  No recent activities.")
        return 0

    for a in items:
        aid = a.get("id", "?")[:8]
        # Get event type from the complex event structure
        event = a.get("event", {})
        event_asset = event.get("asset", {})
        id_pair = event_asset.get("identifier_description_pair", {})
        # Find which event key indicates the action type
        action = "?"
        for k, v in id_pair.items():
            if v not in ("UNKNOWN", None):
                action = k.replace("_", " ")
                break
        created = _readable(a.get("created", {}))
        # Get associated asset name
        asset = a.get("asset", {}) or {}
        asset_name = asset.get("name", "")
        details = f" on '{asset_name}'" if asset_name else ""
        print(f"  [{aid}] {action}{details}  ({created})")
    return 0


def cmd_users():
    """Show connected users and applications."""
    data = api("GET", "/users")
    users = data.get("iterable", []) if data else []
    app_data = api("GET", "/applications")
    apps = app_data.get("iterable", []) if app_data else []
    tags_data = api("GET", "/tags")
    tags = tags_data.get("iterable", []) if tags_data else []

    print(f"  Users: {len(users)}")
    for u in users:
        uid = u.get("id", "?")[:12]
        email = u.get("email", "?")
        username = u.get("username", "")
        name_part = f" ({username})" if username else ""
        print(f"    [{uid}] {email}{name_part}")

    print(f"\n  Applications: {len(apps)}")
    for a in apps:
        print(f"    {a.get('name','?')} v{a.get('version','?')} ({a.get('platform','?')})")

    print(f"\n  Tags: {len(tags)}")
    for t in tags[:5]:
        print(f"    #{t.get('text','?')}")
    if len(tags) > 5:
        print(f"    ... and {len(tags)-5} more")
    return 0


def cmd_summaries():
    """Show workstream summaries (Pieces OS embedded AI)."""
    data = api("GET", "/workstream_summaries?limit=5")
    if data is None:
        return 1

    items = data.get("iterable", [])
    if not items:
        print("  No workstream summaries.")
        return 0

    for s in items:
        sid = s.get("id", "?")[:8]
        title = s.get("name", "Untitled Summary") or "Untitled Summary"
        created = _readable(s.get("created", {}))
        # Get annotations count as a proxy for content
        annotations = s.get("annotations", {}).get("iterable", [])
        model_name = s.get("model", {}).get("name", "")
        model_info = f" [{model_name}]" if model_name else ""
        print(f"  [{sid}] {title}{model_info}")
        print(f"        annotations: {len(annotations)}  |  ({created})")
    return 0


# ── CLI entry point ───────────────────────────────────────────────

USAGE = textwrap.dedent("""\
  Pieces OS CLI — manage long-term memory

  Usage:
    pieces <command> [args]

  Commands:
    status                    Check Pieces OS connectivity
    list                      List memory assets
    search <query>            Search assets by text
    create <text>             Create a new memory asset
    models                    List available AI models
    activities                Show recent activities
    users                     Show connected users & apps
    summaries                 Show workstream summaries
    help                      Show this help text
""")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("help", "--help", "-h"):
        print(USAGE.strip())
        return 0

    cmd = args[0]
    rest = args[1:]

    dispatch = {
        "status":     lambda: cmd_status(),
        "list":       lambda: cmd_list(),
        "search":     lambda: cmd_search(" ".join(rest)) if rest else sys.exit(cmd_help("search <query>")),
        "create":     lambda: cmd_create(" ".join(rest)) if rest else sys.exit(cmd_help("create <text>")),
        "models":     lambda: cmd_models(),
        "activities": lambda: cmd_activities(),
        "users":      lambda: cmd_users(),
        "summaries":  lambda: cmd_summaries(),
    }

    handler = dispatch.get(cmd)
    if handler is None:
        print(f"  Unknown command: {cmd}", file=sys.stderr)
        print(USAGE.strip(), file=sys.stderr)
        return 1

    return handler() or 0


def cmd_help(hint: str):
    print(f"  Usage: pieces {hint}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
