import React, { useEffect, useState } from "react";
import { getJobs, fetchJobs } from "./api";
import "./index.css";

function App() {
  const [jobs, setJobs] = useState([]);
  const [query, setQuery] = useState("Software Engineer");
  const [location, setLocation] = useState("New York, NY");
  const [skill, setSkill] = useState("");
  const [loading, setLoading] = useState(false);
  const [scrapeMsg, setScrapeMsg] = useState("");

  useEffect(() => {
    loadJobs();
    // eslint-disable-next-line
  }, []);

  const loadJobs = async () => {
    setLoading(true);
    try {
      const jobs = await getJobs(skill);
      setJobs(jobs || []);
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async (e) => {
    e.preventDefault();
    setScrapeMsg("Starting scrape...");
    setLoading(true);
    try {
      await fetchJobs(query, location);
      setScrapeMsg("Scrape complete! Loading jobs...");
      await loadJobs();
    } catch (err) {
      console.error(err);
      setScrapeMsg("Scrape failed: " + (err.message || err));
    } finally {
      setScrapeMsg("");
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "32px" }}>
      <h1>
        Job Market Analyzer &mdash; <span style={{ fontWeight: 400 }}>Demo</span>
      </h1>

      <form onSubmit={handleScrape} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search query (e.g. Software Engineer)"
          style={{ marginRight: 8 }}
        />
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location (e.g. New York, NY)"
          style={{ marginRight: 8 }}
        />
        <button type="submit" disabled={loading} style={{ marginRight: "10px" }}>
          Scrape (fetch new jobs)
        </button>
        <input
          type="text"
          value={skill}
          onChange={(e) => setSkill(e.target.value)}
          placeholder="filter by skill (optional)"
          style={{ marginRight: "10px" }}
        />
        <button type="button" onClick={loadJobs} disabled={loading}>
          Load Jobs
        </button>
      </form>

      {scrapeMsg && (
        <div style={{ marginBottom: 16, color: "#007bff" }}>{scrapeMsg}</div>
      )}
      {loading && <div style={{ marginBottom: 16 }}>Loading...</div>}

      <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
        {jobs.length === 0 && !loading && (
          <div style={{ color: "#888", fontSize: "1.1em" }}>No jobs found.</div>
        )}

        {jobs.map((job, idx) => (
          <div
            key={idx}
            style={{ border: "1px solid #ccc", borderRadius: 8, padding: 16, width: 350, background: "#fafbfc" }}
          >
            <a
              href={job.url || job.raw_url}
              target="_blank"
              rel="noreferrer"
              style={{ fontWeight: "bold", fontSize: "1.1em", color: "#222" }}
            >
              {job.title || "No Title"}
            </a>

            <div style={{ margin: "8px 0" }}>
              <span>{job.company || "Unknown Company"}</span>
              {job.location && <span> &mdash; {job.location}</span>}
            </div>

            {job.date_posted && (
              <div style={{ color: "#888", fontSize: "0.9em" }}>
                Posted: {job.date_posted.slice(0, 10)}
              </div>
            )}

            {job.tags && job.tags.length > 0 && (
              <div style={{ margin: "8px 0", color: "#007bff" }}>
                Skills: {Array.isArray(job.tags) ? job.tags.join(", ") : job.tags}
              </div>
            )}

            {job.description && (
              <div style={{ marginTop: 8, fontSize: "0.95em" }}>
                {job.description.length > 300 ? job.description.slice(0, 300) + "..." : job.description}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
