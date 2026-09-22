import JobCard from "./JobCard";

const SUGGESTIONS = ["engineer", "designer", "python", "product manager"];

const STEPS = [
  {
    title: "Type a keyword",
    description: "A role, a skill, a title — whatever you're hunting for.",
  },
  {
    title: "We scan every source live",
    description: "RemoteOK, Jobicy, We Work Remotely, and direct company boards.",
  },
  {
    title: "Results stream in as they're found",
    description: "No refresh needed — matches appear the moment they're scraped.",
  },
];

function RadarMark() {
  return (
    <svg viewBox="0 0 64 64" className="radar-mark" aria-hidden="true">
      <circle cx="32" cy="32" r="28" className="radar-ring" />
      <circle cx="32" cy="32" r="18" className="radar-ring" />
      <circle cx="32" cy="32" r="8" className="radar-ring" />
      <circle cx="32" cy="32" r="2.5" className="radar-dot" />
    </svg>
  );
}

export default function JobList({ jobs, status, keywords, hasSearched, onSearch }) {
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
      <div className="empty-panel">
        <div className="empty-primary">
          <RadarMark />
          <h2>Nothing scanned yet</h2>
          <p>Enter a keyword on the left to start a live search.</p>
          <div className="suggestion-block">
            <span className="suggestion-label">Try</span>
            <div className="suggestion-chips">
              {SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  className="suggestion-chip"
                  onClick={() => onSearch(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="empty-divider" />

        <ol className="empty-steps">
          {STEPS.map((step, index) => (
            <li key={step.title}>
              <span className="step-number">{index + 1}</span>
              <div>
                <p className="step-title">{step.title}</p>
                <p className="step-description">{step.description}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    );
  }

  return (
    <div className="job-grid">
      {jobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
