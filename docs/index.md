# URL Watcher Documentation

Welcome to URL Watcher — an async FastAPI service that monitors URLs and records their status, latency, and errors.

## Features

- **Async monitoring**: Non-blocking HTTP checks using `httpx`
- **REST API**: Add, list, and manage monitored URLs
- **Background workers**: Continuous URL monitoring at configurable intervals
- **Persistent storage**: SQLite for demo, PostgreSQL for production
- **CI/CD ready**: GitHub Actions, Docker, and automated deployments

## Quick Links

- **Live Demo**: (add your deployed URL here)
- **GitHub Repo**: https://github.com/thenmozhibathu98/url-watcher
- **API Docs**: Visit `/docs` on your deployed instance
- **Interactive Swagger UI**: Available at `/docs` endpoint

## Getting Started

See the README.md for local setup and API examples.

## Architecture

- **Backend**: FastAPI + asyncio
- **Database**: SQLModel ORM
- **Async Client**: httpx
- **Container**: Docker
- **CI/CD**: GitHub Actions → Docker image → Deployment

## Next Steps

- Add monitors via the API
- View check history for each monitor
- Deploy to production (Render, Heroku, or AWS)
- Set up alerts and notifications
