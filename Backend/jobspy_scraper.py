from jobspy_local import scrape_jobs
from sqlalchemy.orm import Session
from datetime import datetime
from crud import create_job
from models import Job


def fetch_and_store_jobs(db: Session, query="Software Engineer", location="New York, NY", results_wanted=20, hours_old=72):
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term=query,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
    )

    if jobs is None:
        return 0

    try:
        iterator = jobs.iterrows()
    except Exception:
        iterator = enumerate(jobs)

    count = 0
    for _, row in iterator:
        get = getattr(row, "get", None)
        if callable(get):
            title = row.get("title", "")
            company = row.get("company", "")
            location_val = row.get("location", "")
            url = row.get("url", "")
            description = row.get("description", "")
            tags = row.get("tags", [])
        else:
            title = row["title"] if "title" in row else ""
            company = row["company"] if "company" in row else ""
            location_val = row["location"] if "location" in row else ""
            url = row["url"] if "url" in row else ""
            description = row["description"] if "description" in row else ""
            tags = row["tags"] if "tags" in row else []

        job_data = type('J', (), {})()
        job_data.title = title
        job_data.company = company
        job_data.location = location_val
        job_data.url = url
        job_data.date_posted = datetime.now()
        job_data.description = description
        job_data.tags = tags

        create_job(db, job_data)
        count += 1

    return count
