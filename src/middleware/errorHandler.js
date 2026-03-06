exports.errorHandler = (err, req, res, next) => {
  console.error(err.stack);

  const status = err.response?.status || 500;
  const message =
    status === 404
      ? "GitHub user not found"
      : status === 403
      ? "GitHub API rate limit exceeded. Add a GITHUB_TOKEN to .env to increase limits."
      : err.message || "Internal server error";

  res.status(status).json({ success: false, error: message });
};
