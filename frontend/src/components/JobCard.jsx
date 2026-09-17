export default function JobCard({ job }) {
  return (
    <a className="job-row" href={job.url} target="_blank" rel="noreferrer">
      <span className="job-title">{job.title}</span>
      <span className="job-meta">
        {job.company}
        {job.location ? `, ${job.location}` : ""}
      </span>
    </a>
  );
}
