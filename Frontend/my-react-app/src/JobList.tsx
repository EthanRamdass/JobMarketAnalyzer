// frontend/src/JobList.jsx
import React, { useEffect, useState, ChangeEvent } from "react";
import { getJobs, fetchJobs as fetchJobsApi } from "./api";

type Job = {
  url: string;
  title: string;
  company: string;
  location: string;
  tags: string[];
};

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [skill, setSkill] = useState<string>("");

  useEffect(() => {
    getJobs().then(setJobs);
  }, []);

  async function fetchJobs() {
    if (skill) {
      const data = await fetchJobsApi(skill, "");
      setJobs(data);
    } else {
      getJobs().then(setJobs);
    }
  }

  return (
    <div>
      <input
        placeholder="filter by skill"
        value={skill}
        onChange={(e: ChangeEvent<HTMLInputElement>) => setSkill(e.target.value)}
      />
      <button onClick={fetchJobs}>Filter</button>
      <ul>
        {jobs.map((j: Job, idx: number) => (
          <li key={idx}>
            <a href={j.url} target="_blank" rel="noreferrer">{j.title}</a> - {j.company} ({j.location})
            <div>{j.tags.join(", ")}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
