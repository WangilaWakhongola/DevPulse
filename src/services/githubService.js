const axios = require("axios");
const NodeCache = require("node-cache");

const cache = new NodeCache({ stdTTL: 300 }); // Cache for 5 minutes

const githubAPI = axios.create({
  baseURL: "https://api.github.com",
  headers: {
    Accept: "application/vnd.github+json",
    ...(process.env.GITHUB_TOKEN && {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
    }),
  },
});

async function cachedGet(key, fetchFn) {
  const cached = cache.get(key);
  if (cached) return cached;
  const data = await fetchFn();
  cache.set(key, data);
  return data;
}

exports.fetchProfile = async (username) => {
  return cachedGet(`profile:${username}`, async () => {
    const { data } = await githubAPI.get(`/users/${username}`);
    return {
      login: data.login,
      name: data.name,
      avatar: data.avatar_url,
      bio: data.bio,
      location: data.location,
      blog: data.blog,
      followers: data.followers,
      following: data.following,
      publicRepos: data.public_repos,
      createdAt: data.created_at,
      url: data.html_url,
    };
  });
};

exports.fetchRepos = async (username, sort = "updated", limit = 6) => {
  return cachedGet(`repos:${username}:${sort}:${limit}`, async () => {
    const { data } = await githubAPI.get(`/users/${username}/repos`, {
      params: { sort, per_page: limit },
    });
    return data.map((repo) => ({
      name: repo.name,
      description: repo.description,
      stars: repo.stargazers_count,
      forks: repo.forks_count,
      language: repo.language,
      url: repo.html_url,
      updatedAt: repo.updated_at,
      topics: repo.topics || [],
    }));
  });
};

exports.fetchActivity = async (username) => {
  return cachedGet(`activity:${username}`, async () => {
    const { data } = await githubAPI.get(`/users/${username}/events/public`, {
      params: { per_page: 10 },
    });
    return data.map((event) => ({
      type: event.type,
      repo: event.repo.name,
      createdAt: event.created_at,
      payload: summarizePayload(event),
    }));
  });
};

exports.fetchStats = async (username) => {
  return cachedGet(`stats:${username}`, async () => {
    const { data: repos } = await githubAPI.get(`/users/${username}/repos`, {
      params: { per_page: 100 },
    });

    const languages = {};
    let totalStars = 0;
    let totalForks = 0;

    repos.forEach((repo) => {
      totalStars += repo.stargazers_count;
      totalForks += repo.forks_count;
      if (repo.language) {
        languages[repo.language] = (languages[repo.language] || 0) + 1;
      }
    });

    const topLanguages = Object.entries(languages)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([lang, count]) => ({ lang, count }));

    return { totalStars, totalForks, topLanguages, totalRepos: repos.length };
  });
};

function summarizePayload(event) {
  switch (event.type) {
    case "PushEvent":
      return `Pushed ${event.payload.commits?.length || 0} commit(s)`;
    case "CreateEvent":
      return `Created ${event.payload.ref_type} ${event.payload.ref || ""}`;
    case "WatchEvent":
      return "Starred a repository";
    case "ForkEvent":
      return "Forked a repository";
    case "IssuesEvent":
      return `${event.payload.action} an issue`;
    case "PullRequestEvent":
      return `${event.payload.action} a pull request`;
    default:
      return event.type.replace("Event", "");
  }
}
