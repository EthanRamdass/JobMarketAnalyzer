const API_URL = "http://localhost:5000/api";

export async function getJobs(skill = "", q = "", page = 0, per_page = 50) {
  const params = new URLSearchParams({ skill, q, page, per_page });
  const res = await fetch(`${API_URL}/jobs?${params}`);
  return res.json();
}

export async function fetchJobs(query = "Software Engineer", location = "New York, NY", results_wanted = 20, hours_old = 72) {
  const res = await fetch(`${API_URL}/jobspy-scrape`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, location, results_wanted, hours_old })
  });
  return res.json();
}
