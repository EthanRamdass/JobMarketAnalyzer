import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
from models import init_db, get_db_session
from crud import query_jobs
from jobspy_scraper import fetch_and_store_jobs
import traceback

load_dotenv()
app = Flask(__name__)
# Allow cross-origin requests from the frontend dev server during development
CORS(app)
init_db()

@app.route("/")
def home():
    return {"message": "Backend is running!"}

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    skill = request.args.get("skill")
    q = request.args.get("q")
    page = int(request.args.get("page", 0))
    per_page = int(request.args.get("per_page", 50))
    offset = page * per_page

    db = get_db_session()
    jobs = query_jobs(db, limit=per_page, offset=offset, skill=skill, q=q) or []
    db.close()

    result = []
    for j in jobs:
        result.append({
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "date_posted": j.date_posted.isoformat() if j.date_posted else None,
            "description": j.description[:500] if j.description else "",
            "url": j.url,
            "tags": j.tags.split(",") if j.tags else []
        })
    return jsonify(result)

@app.route("/api/jobspy-scrape", methods=["POST"])
def jobspy_scrape():
    body = request.json or {}
    query = body.get("query", "Software Engineer")
    location = body.get("location", "New York, NY")
    results_wanted = int(body.get("results_wanted", 20))
    hours_old = int(body.get("hours_old", 72))

    db = get_db_session()
    try:
        count = fetch_and_store_jobs(db, query=query, location=location, results_wanted=results_wanted, hours_old=hours_old)
        db.close()
        return jsonify({"status": "ok", "query": query, "location": location, "inserted": count})
    except Exception as e:
        # Log traceback to console for debugging in the terminal where Flask is running
        traceback.print_exc()
        db.close()
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
