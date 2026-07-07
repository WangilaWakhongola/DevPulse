# DevPulse : GitHub Activity Dashboard

A real-time GitHub developer dashboard built with **Python & Flask**.  
Search any GitHub username and instantly visualize their profile, repositories, language stats, and activity feed.

> Python rewrite of the original Node.js/Express version.

--

## Features

- **Profile Overview** — Avatar, bio, location, follower/following count
- **Top Repositories** — Most recently updated repos with language, stars, forks & topics
- **Language Breakdown** — Visual bar chart of most-used languages across all repos
- **Activity Feed** — Real-time public events (pushes, PRs, stars, forks, etc.)
- **Rate Limiting** — 100 requests per 15 minutes per IP (via Flask-Limiter)
- **In-Memory Caching** — 5-minute TTL cache to protect GitHub API rate limits
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, XSS Protection, etc.

---

## Project Structure

```
devpulse/
├── src/
│   ├── app.py                        # Flask entry point
│   ├── routes/
│   │   └── github.py                 # URL route definitions
│   ├── controllers/
│   │   └── github_controller.py      # Request handlers
│   ├── services/
│   │   └── github_service.py         # GitHub API calls + caching
│   └── middleware/
│       ├── error_handler.py          # Global error handler
│       └── rate_limiter.py           # Request rate limiting
├── public/
│   └── index.html                    # Frontend single-page app
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DevPulse.git
cd DevPulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and optionally add your GitHub token:

```
PORT=3000
GITHUB_TOKEN=ghp_your_personal_access_token_here
FLASK_ENV=development
```

> Generate a token at: **GitHub → Settings → Developer Settings → Personal Access Tokens**  
> Only the `public_repo` read scope is needed. Without a token, GitHub limits you to 60 requests/hour; with one, it's 5000/hour.

### 5. Run the app

```bash
# From the project root
python src/app.py
```

Open **http://localhost:3000** in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/github/:username/profile` | User profile data |
| GET | `/api/github/:username/repos` | Public repositories |
| GET | `/api/github/:username/activity` | Recent public events |
| GET | `/api/github/:username/stats` | Aggregated stats & language breakdown |

**Query params for `/repos`:**

- `sort` — `updated` (default), `stars`, `created`
- `limit` — number of repos to return (default: `6`)

---

## How It Works

1. The **frontend** (`public/index.html`) sends fetch requests to the Flask API with a GitHub username
2. The **routes** map URL patterns to controller functions
3. The **controller** validates the request and delegates to the **service** layer
4. The **service** checks an in-memory **cache** (5-min TTL) before calling the GitHub REST API
5. Results are returned as JSON and rendered dynamically in the browser

---

## Comparison with Original

| Feature | Original (Node.js) | This Version (Python) |
|---|---|---|
| Runtime | Node.js 18+ | Python 3.8+ |
| Framework | Express 4.x | Flask 3.x |
| HTTP client | Axios | Requests |
| Caching | node-cache | In-memory dict with TTL |
| Rate limiting | express-rate-limit | Flask-Limiter |
| Security headers | Helmet.js | Custom after_request hook |
| Config | dotenv (npm) | python-dotenv |

---

## Ideas to Extend

- [ ] Contribution graph using GitHub's contribution API
- [ ] Compare two developers side-by-side
- [ ] Export profile as PDF or image card
- [ ] OAuth login to view private repo stats
- [ ] Deploy to Railway, Render, or Fly.io

---

## Author

**Emmanuel Wakhongola**
- GitHub: [@WangilaWakhongola](https://github.com/WangilaWakhongola)
- Email: wangilaemmanuel06@gmail.com

## License

MIT — feel free to fork and build on top of this!
