const express = require("express");
const router = express.Router();
const githubController = require("../controllers/githubController");

// GET /api/github/:username/profile
router.get("/:username/profile", githubController.getProfile);

// GET /api/github/:username/repos
router.get("/:username/repos", githubController.getRepos);

// GET /api/github/:username/activity
router.get("/:username/activity", githubController.getActivity);

// GET /api/github/:username/stats
router.get("/:username/stats", githubController.getStats);

module.exports = router;
