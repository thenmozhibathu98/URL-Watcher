# URL Watcher

URL Watcher — an async FastAPI service that monitors URLs, records status & latency, and exposes an API to manage monitors.

Live demo: https://url-watcher.onrender.com/docs

Badges
- Build:[![CI](https://github.com/thenmozhibathu98/URL-Watcher/actions/workflows/ci.yml/badge.svg)]
- Docs: (https://github.com/thenmozhibathu98/URL-Watcher.git)

Quick start (local)
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload --port 8000
4. Open http://localhost:8000/docs for the interactive API docs

Docker
- Build: docker build -t url-watcher:local .
- Run: docker run -p 8000:8000 url-watcher:local

What to look for
- CI runs tests on PRs and pushes.
- Docker image is published to GHCR on pushes to main.
- Documentation site is published to GitHub Pages automatically.

Contacts
- Author: thenmozhibathu98

### Run locally

```bash
# Clone the repo
git clone https://github.com/thenmozhibathu98/url-watcher.git
cd url-watcher

# Create virtual environment
python -m venv . venv
. venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload --port 8000
