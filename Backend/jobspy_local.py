"""A thin local wrapper around the external `jobspy` package.

This file previously contained a recursive import and duplicated code which caused
imports to fail. Keep this wrapper minimal: import the real `scrape_jobs` from the
installed `jobspy` package and re-export it as `scrape_jobs` so other modules can
call it uniformly.
"""

from datetime import datetime
from typing import Any

try:
    # Import the real jobspy function provided by the external package.
    from jobspy import scrape_jobs  # type: ignore
except Exception as e:
    # If jobspy is not installed, provide a helpful fallback that raises when used.
    def scrape_jobs(*args, **kwargs):  # type: ignore
        raise RuntimeError("jobspy is not installed or failed to import: " + str(e))


# Keep a tiny compatibility wrapper signature if callers expect the same params.
def scrape_jobs_wrapper(site_name=None, search_term=None, location=None, results_wanted=20, hours_old=72) -> Any:
    """Call the jobspy.scrape_jobs and return whatever it produces (usually a DataFrame).

    We keep this wrapper so calling code can import `scrape_jobs` from this module
    (as used by `jobspy_scraper.py`).
    """
    return scrape_jobs(
        site_name=site_name,
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
    )


# Re-export with the expected name used elsewhere in the codebase.
scrape_jobs = scrape_jobs_wrapper
