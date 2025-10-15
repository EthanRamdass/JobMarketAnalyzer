"""Wrapper around jobspy to support local scraping if installed.
If jobspy is not available, this returns an empty list to keep the app running.
"""
try:
    from jobspy import search as _jobspy_search
except Exception:
    _jobspy_search = None

def scrape_jobs(site_name=None, search_term=None, location=None, results_wanted=20, hours_old=72):
    if _jobspy_search is None:
        # jobspy not installed; return empty list
        return []
    return _jobspy_search(site=site_name, query=search_term, location=location, limit=results_wanted)
