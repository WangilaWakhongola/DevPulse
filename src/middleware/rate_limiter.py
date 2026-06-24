"""
Rate Limiter Middleware
Limits each IP to 100 requests per 15 minutes.
Equivalent to src/middleware/rateLimiter.js (express-rate-limit)
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per 15 minutes"],
    storage_uri="memory://",
)
