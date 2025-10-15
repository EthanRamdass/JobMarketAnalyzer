from .jobspy_local import scrape_jobs
from sqlalchemy.orm import Session
from datetime import datetime
from . import crud
from . import schemas


def fetch_and_store_jobs(db: Session, query="Software Engineer", location="New York, NY", results_wanted=20, hours_old=72):
    # Call the wrapper; it will raise a descriptive error if jobspy isn't installed
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term=query,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
    )

    # Some jobspy versions return a pandas.DataFrame; if jobs is None, do nothing
    if jobs is None:
        return 0

    # If it's a DataFrame-like object, iterate rows; otherwise, try to iterate records
    try:
        iterator = jobs.iterrows()
    except Exception:
        iterator = enumerate(jobs)

    count = 0
    for _, row in iterator:
        # row might be a pandas Series or a dict-like object
        get = getattr(row, "get", None)
        if callable(get):
            title = row.get("title", "")
            company = row.get("company", "")
            location_val = row.get("location", "")
            url = row.get("url", "")
            description = row.get("description", "")
            tags = row.get("tags", [])
        else:
            # assume mapping-like via [] access
            title = row["title"] if "title" in row else ""
            company = row["company"] if "company" in row else ""
            location_val = row["location"] if "location" in row else ""
            url = row["url"] if "url" in row else ""
            description = row["description"] if "description" in row else ""
            tags = row["tags"] if "tags" in row else []

        job = schemas.JobCreate(
            title=title,
            company=company,
            location=location_val,
            url=url,
            date_posted=datetime.now(),
            description=description,
            tags=tags or [],
        )
        crud.create_job(db, job)
        count += 1

    return count