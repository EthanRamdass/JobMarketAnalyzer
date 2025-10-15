from Backend.jobspy_local import scrape_jobs
from sqlalchemy.orm import Session
from datetime import datetime
from . import crud
from . import schemas

def fetch_and_store_jobs(db: Session, query="Software Engineer", location="New York, NY", results_wanted=20, hours_old=72):
    jobs = scrape_jobs(
        site_name=["indeed"],  # Change to your preferred site(s)
        search_term=query,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
    )

    for _, row in jobs.iterrows():
        job = schemas.JobCreate(
            title=row.get("title", ""),
            company=row.get("company", ""),
            location=row.get("location", ""),
            url=row.get("url", ""),
            date_posted=datetime.now(),
            description=row.get("description", ""),
            tags=row.get("tags", [])
        )
        crud.create_job(db, job)