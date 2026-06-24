"""
Error Handler Middleware
Global error handling for Flask.
Equivalent to src/middleware/errorHandler.js
"""

from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Route not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "error": "Method not allowed"}), 405

    @app.errorhandler(429)
    def too_many_requests(e):
        return jsonify({"success": False, "error": "Too many requests — slow down!"}), 429

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500
