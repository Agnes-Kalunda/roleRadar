import JobCard from "./JobCard";

export default function JobList({ jobs, status, keywords, hasSearched }) {
  if (jobs.length === 0 && status === "searching") {
    return (
      <div className="scanning">
        <span className="scan-bar" />
        <p>Scanning boards for &ldquo;{keywords}&rdquo;&hellip;</p>
      </div>
    );
  }

  if (jobs.length === 0 && hasSearched) {
    return (
      <div className="empty">
        <p>No matches found for &ldquo;{keywords}&rdquo;.</p>
        <p>Try a broader or different keyword.</p>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="empty">
        <p>No matches yet.</p>
        <p>Enter a keyword and results will appear here as they're found.</p>
      </div>
    );
  }

  return (
    <div className="ledger-list">
      {jobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
