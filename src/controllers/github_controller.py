"""
GitHub Controller
Handles incoming requests and delegates to the GitHub service.
Equivalent to src/controllers/githubController.js
"""

from flask import jsonify, request
from services.github_service import get_profile, get_repos, get_activity, get_stats


def profile(username: str):
    try:
        data = get_profile(username)
        return jsonify({"success": True, "data": data})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"success": False, "error": str(e)}), 403
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to fetch profile"}), 500


def repos(username: str):
    sort = request.args.get("sort", "updated")
    try:
        limit = int(request.args.get("limit", 6))
    except ValueError:
        limit = 6

    if sort not in ("updated", "stars", "created"):
        sort = "updated"

    try:
        data = get_repos(username, sort=sort, limit=limit)
        return jsonify({"success": True, "data": data})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"success": False, "error": str(e)}), 403
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to fetch repositories"}), 500


def activity(username: str):
    try:
        data = get_activity(username)
        return jsonify({"success": True, "data": data})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"success": False, "error": str(e)}), 403
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to fetch activity"}), 500


def stats(username: str):
    try:
        data = get_stats(username)
        return jsonify({"success": True, "data": data})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"success": False, "error": str(e)}), 403
    except Exception as e:
        return jsonify({"success": False, "error": "Failed to fetch stats"}), 500
