# Job Market Analyzer

**Tech:** Python, Flask, SQLAlchemy, SQLite (or PostgreSQL), Docker, JobSpy, React (Vite), REST, JSON

A full-stack application that automatically aggregates job postings from multiple sources, normalizes and stores them in a relational database, and exposes REST APIs for searching, filtering, and visualization. Designed as a reproducible, containerized app to demonstrate end-to-end backend + data engineering capabilities.

---

## Features
- Scrapes job postings (via `jobspy` + custom scraping logic), normalizes fields (title, company, location, tags).
- Persists structured results in a relational database (SQLite for local dev, easy to swap for Postgres).
- REST API endpoints for searching, filtering, and paginating job results.
- Simple React frontend to query and display job listings.
- Docker + `docker-compose` for reproducible local deployment.

---

## Tech Stack
- Backend: Python, Flask, SQLAlchemy, python-dotenv, JobSpy
- Frontend: React (Vite)
- Database: SQLite (dev) / PostgreSQL (prod)
- Deployment: Docker, docker-compose
- Data format: JSON (REST)

---

## Quickstart (local, without Docker)

> Make sure you are in the `backend/` folder and you have Python 3.9+ installed.

```bash
# Create and activate venv
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# Install backend deps
pip install -r requirements.txt

# Initialize DB
python init_db.py

# Start backend
python app.py
# Backend API available at http://localhost:5000
