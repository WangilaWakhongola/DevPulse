"""
GitHub Routes
Registers all /api/github/* endpoints.
Equivalent to src/routes/github.js
"""

from flask import Blueprint
from controllers.github_controller import profile, repos, activity, stats

github_bp = Blueprint("github", __name__)

github_bp.add_url_rule("/<username>/profile",  view_func=profile,  methods=["GET"])
github_bp.add_url_rule("/<username>/repos",    view_func=repos,    methods=["GET"])
github_bp.add_url_rule("/<username>/activity", view_func=activity, methods=["GET"])
github_bp.add_url_rule("/<username>/stats",    view_func=stats,    methods=["GET"])
