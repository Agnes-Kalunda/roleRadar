import JobCard from "./JobCard";

export default function JobList({ jobs }) {
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
