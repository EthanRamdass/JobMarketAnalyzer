from .models import Job
from sqlalchemy.orm import Session

def create_job(db: Session, job_data):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        url=job_data.url,
        date_posted=job_data.date_posted,
        description=job_data.description,
        tags=",".join(job_data.tags) if job_data.tags else ""
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def query_jobs(db: Session, limit=50, offset=0, skill=None, q=None):
    query = db.query(Job)
    if skill:
        query = query.filter(Job.tags.like(f"%{skill}%"))
    if q:
        query = query.filter(Job.title.like(f"%{q}%"))
    return query.offset(offset).limit(limit).all()