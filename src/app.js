require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const morgan = require("morgan");
const path = require("path");

const githubRoutes = require("./routes/github");
const { errorHandler } = require("./middleware/errorHandler");
const { rateLimiter } = require("./middleware/rateLimiter");

const app = express();
const PORT = process.env.PORT || 3000;

// Security & logging middleware
app.use(helmet({ contentSecurityPolicy: false }));
app.use(morgan("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use(express.static(path.join(__dirname, "../public")));

// Rate limiting
app.use("/api", rateLimiter);

// Routes
app.use("/api/github", githubRoutes);

// Serve main HTML
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Error handler
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`🚀 DevPulse running at http://localhost:${PORT}`);
});

module.exports = app;
