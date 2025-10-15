# backend/store.py
from .models import SessionLocal, Job
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def save_job(job_data):
    """
    Save a job dict into the DB. job_data keys:
      job_id, title, company, location, date_posted, description, raw_url, tags
    """
    db = SessionLocal()
    job = Job(**job_data)
    try:
        db.add(job)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
    finally:
        db.close()

def query_jobs(limit=50, offset=0, skill=None, q=None):
    db = SessionLocal()
    query = db.query(Job)
    if skill:
        query = query.filter(Job.tags.ilike(f"%{skill}%"))
    if q:
        qterm = f"%{q}%"
        query = query.filter((Job.title.ilike(qterm)) | (Job.description.ilike(qterm)))
    results = query.order_by(Job.date_posted.desc()).offset(offset).limit(limit).all()
    db.close()
    return results

