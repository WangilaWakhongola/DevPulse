"""
GitHub Service
Handles all GitHub API requests with in-memory caching (5-minute TTL).
Equivalent to src/services/githubService.js
"""

import os
import time
import requests
from threading import Lock

GITHUB_API = "https://api.github.com"
CACHE_TTL = 300  # 5 minutes

_cache: dict = {}
_lock = Lock()


def _get_headers() -> dict:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _cache_get(key: str):
    with _lock:
        entry = _cache.get(key)
        if entry and (time.time() - entry["ts"]) < CACHE_TTL:
            return entry["data"]
        return None


def _cache_set(key: str, data):
    with _lock:
        _cache[key] = {"data": data, "ts": time.time()}


def _github_get(path: str) -> dict | list:
    """Make a GET request to the GitHub API, raising on error."""
    url = f"{GITHUB_API}{path}"
    response = requests.get(url, headers=_get_headers(), timeout=10)
    if response.status_code == 404:
        raise ValueError(f"GitHub user or resource not found: {path}")
    if response.status_code == 403:
        raise PermissionError("GitHub API rate limit exceeded. Add a GITHUB_TOKEN to your .env file.")
    response.raise_for_status()
    return response.json()


# ── Public API ────────────────────────────────────────────────────────────────

def get_profile(username: str) -> dict:
    key = f"profile:{username}"
    cached = _cache_get(key)
    if cached:
        return cached

    data = _github_get(f"/users/{username}")
    result = {
        "login": data.get("login"),
        "name": data.get("name"),
        "avatar_url": data.get("avatar_url"),
        "bio": data.get("bio"),
        "location": data.get("location"),
        "company": data.get("company"),
        "blog": data.get("blog"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "created_at": data.get("created_at"),
        "html_url": data.get("html_url"),
    }
    _cache_set(key, result)
    return result


def get_repos(username: str, sort: str = "updated", limit: int = 6) -> list:
    key = f"repos:{username}:{sort}:{limit}"
    cached = _cache_get(key)
    if cached:
        return cached

    data = _github_get(f"/users/{username}/repos?sort={sort}&per_page=100&type=owner")
    repos = []
    for r in data[:limit]:
        repos.append({
            "id": r.get("id"),
            "name": r.get("name"),
            "full_name": r.get("full_name"),
            "description": r.get("description"),
            "html_url": r.get("html_url"),
            "language": r.get("language"),
            "stargazers_count": r.get("stargazers_count"),
            "forks_count": r.get("forks_count"),
            "topics": r.get("topics", []),
            "updated_at": r.get("updated_at"),
            "created_at": r.get("created_at"),
        })
    _cache_set(key, repos)
    return repos


def get_activity(username: str) -> list:
    key = f"activity:{username}"
    cached = _cache_get(key)
    if cached:
        return cached

    data = _github_get(f"/users/{username}/events/public?per_page=30")
    events = []
    for e in data:
        events.append({
            "id": e.get("id"),
            "type": e.get("type"),
            "repo": e.get("repo", {}).get("name"),
            "created_at": e.get("created_at"),
            "payload_summary": _summarise_payload(e),
        })
    _cache_set(key, events)
    return events


def get_stats(username: str) -> dict:
    key = f"stats:{username}"
    cached = _cache_get(key)
    if cached:
        return cached

    repos_raw = _github_get(f"/users/{username}/repos?per_page=100&type=owner")

    lang_counts: dict[str, int] = {}
    total_stars = 0
    total_forks = 0

    for r in repos_raw:
        lang = r.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        total_stars += r.get("stargazers_count", 0)
        total_forks += r.get("forks_count", 0)

    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)

    result = {
        "total_repos": len(repos_raw),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "languages": [{"name": l, "count": c} for l, c in sorted_langs],
    }
    _cache_set(key, result)
    return result


# ── Helpers ───────────────────────────────────────────────────────────────────

def _summarise_payload(event: dict) -> str:
    t = event.get("type", "")
    p = event.get("payload", {})
    repo = event.get("repo", {}).get("name", "")

    if t == "PushEvent":
        commits = len(p.get("commits", []))
        return f"Pushed {commits} commit(s) to {repo}"
    if t == "PullRequestEvent":
        action = p.get("action", "")
        pr = p.get("pull_request", {}).get("title", "")
        return f"{action.capitalize()} PR: {pr}"
    if t == "IssuesEvent":
        action = p.get("action", "")
        title = p.get("issue", {}).get("title", "")
        return f"{action.capitalize()} issue: {title}"
    if t == "WatchEvent":
        return f"Starred {repo}"
    if t == "ForkEvent":
        return f"Forked {repo}"
    if t == "CreateEvent":
        ref_type = p.get("ref_type", "")
        ref = p.get("ref", "")
        return f"Created {ref_type} {ref} in {repo}"
    if t == "DeleteEvent":
        ref_type = p.get("ref_type", "")
        return f"Deleted {ref_type} in {repo}"
    return t.replace("Event", "")
