# 🚀 DevPulse — GitHub Activity Dashboard

> A real-time GitHub developer dashboard built with Node.js & Express.  
> Search any GitHub username and instantly visualize their profile, repositories, language stats, and activity feed.

![Node.js](https://img.shields.io/badge/Node.js-18%2B-green?style=flat-square)
![Express](https://img.shields.io/badge/Express-4.x-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)

---

## ✨ Features

- 🔍 **Profile Overview** — Avatar, bio, location, follower/following count
- 📦 **Top Repositories** — Most recently updated repos with language, stars, forks & topics
- 📊 **Language Breakdown** — Visual bar chart of your most-used languages
- ⚡ **Activity Feed** — Real-time public events (pushes, PRs, stars, forks)
- 🛡️ **Rate Limiting & Caching** — Protects GitHub API limits with 5-min response cache
- 🔒 **Security Headers** — Powered by Helmet.js

---

## 🗂️ Project Structure

```
devpulse/
├── src/
│   ├── app.js                  # Express entry point
│   ├── routes/
│   │   └── github.js           # API route definitions
│   ├── controllers/
│   │   └── githubController.js # Request handlers
│   ├── services/
│   │   └── githubService.js    # GitHub API calls + caching
│   └── middleware/
│       ├── errorHandler.js     # Global error handler
│       └── rateLimiter.js      # Request rate limiting
├── public/
│   └── index.html              # Frontend (single-file SPA)
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

---

## 🛠️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/devpulse.git
cd devpulse
```

### 2. Install dependencies

```bash
npm install
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your GitHub token (optional but recommended to avoid rate limits):

```
PORT=3000
GITHUB_TOKEN=ghp_your_personal_access_token
```

> 💡 Generate a token at: **GitHub → Settings → Developer Settings → Personal Access Tokens**  
> Only `public_repo` read scope is needed.

### 4. Run the app

```bash
# Development (with auto-reload)
npm run dev

# Production
npm start
```

Open **http://localhost:3000** in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/github/:username/profile` | User profile data |
| GET | `/api/github/:username/repos` | Public repositories |
| GET | `/api/github/:username/activity` | Recent public events |
| GET | `/api/github/:username/stats` | Aggregated stats & languages |

**Query params for `/repos`:**
- `sort` — `updated` (default), `stars`, `created`
- `limit` — number of repos to return (default: `6`)

---

## 🧠 How It Works

1. **Frontend** sends requests to the Express API with the GitHub username
2. **Controller** receives the request and delegates to the **Service** layer
3. **Service** checks the in-memory **cache** (5 min TTL) before hitting the GitHub API
4. Results are returned as JSON and rendered dynamically on the page

---

## 🚀 Ideas to Extend

- [ ] Add contribution graph using GitHub's contribution API
- [ ] Compare two developers side-by-side
- [ ] Export profile as PDF / PNG card
- [ ] Add OAuth login to view private repo stats
- [ ] Deploy to Render / Railway / Fly.io

---

## 📄 License

MIT — feel free to fork and build on top of this!
