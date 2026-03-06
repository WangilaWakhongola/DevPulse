const githubService = require("../services/githubService");

exports.getProfile = async (req, res, next) => {
  try {
    const { username } = req.params;
    const profile = await githubService.fetchProfile(username);
    res.json({ success: true, data: profile });
  } catch (err) {
    next(err);
  }
};

exports.getRepos = async (req, res, next) => {
  try {
    const { username } = req.params;
    const { sort = "updated", limit = 6 } = req.query;
    const repos = await githubService.fetchRepos(username, sort, parseInt(limit));
    res.json({ success: true, data: repos });
  } catch (err) {
    next(err);
  }
};

exports.getActivity = async (req, res, next) => {
  try {
    const { username } = req.params;
    const activity = await githubService.fetchActivity(username);
    res.json({ success: true, data: activity });
  } catch (err) {
    next(err);
  }
};

exports.getStats = async (req, res, next) => {
  try {
    const { username } = req.params;
    const stats = await githubService.fetchStats(username);
    res.json({ success: true, data: stats });
  } catch (err) {
    next(err);
  }
};
