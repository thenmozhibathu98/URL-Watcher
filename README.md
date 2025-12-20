# URL Watcher

![CI](https://github.com/thenmozhibathu98/url-watcher/actions/workflows/ci.yml/badge.svg)

A simple, async FastAPI service that monitors URLs on configurable intervals, records HTTP status codes, latency, and errors.  Exposes a REST API to manage monitors and view check history.

**Live demo**: (coming soon after deployment)

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- pip

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