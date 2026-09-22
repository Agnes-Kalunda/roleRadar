function timeAgoLabel(scrapedAt) {
  if (!scrapedAt) return "";
  const scraped = new Date(scrapedAt);
  const now = new Date();
  const daysAgo = Math.floor((now - scraped) / (1000 * 60 * 60 * 24));

  if (daysAgo <= 0) return "Posted today";
  if (daysAgo === 1) return "Posted yesterday";
  return `Posted ${daysAgo} days ago`;
}

function isRecent(scrapedAt) {
  if (!scrapedAt) return false;
  const hoursAgo = (new Date() - new Date(scrapedAt)) / (1000 * 60 * 60);
  return hoursAgo <= 24;
}

export default function JobCard({ job }) {
  const tags = (job.tags || "")
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

  const visibleTags = tags.slice(0, 3);
  const extraTagCount = tags.length - visibleTags.length;

  return (
    <article className="job-card">
      <div className="job-card-badges">
        <span className="badge badge-posted">{timeAgoLabel(job.scraped_at)}</span>
        {isRecent(job.scraped_at) && <span className="badge badge-new">New</span>}
      </div>

      <h3 className="job-card-title">{job.title}</h3>
      <p className="job-card-meta">
        {job.company}
        {job.location ? ` · ${job.location}` : ""}
      </p>

      {visibleTags.length > 0 && (
        <div className="job-card-tags">
          {visibleTags.map((tag) => (
            <span className="tag-chip" key={tag}>
              {tag}
            </span>
          ))}
          {extraTagCount > 0 && (
            <span className="tag-chip tag-chip-more">+{extraTagCount}</span>
          )}
        </div>
      )}

      <a className="apply-button" href={job.url} target="_blank" rel="noreferrer">
        Apply now
      </a>
    </article>
  );
}
