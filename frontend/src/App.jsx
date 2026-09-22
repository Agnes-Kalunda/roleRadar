import { useState } from "react";
import { useJobSearch } from "./hooks/useJobSearch";
import SearchBar from "./components/SearchBar";
import JobList from "./components/JobList";

const STATUS_LABELS = {
  connecting: "Connecting",
  idle: "Ready",
  searching: "Scanning",
  disconnected: "Disconnected",
};

export default function App() {
  const { jobs, status, keywords, hasSearched, search, resetSearch } = useJobSearch();
  const [resetSignal, setResetSignal] = useState(0);

  function handleClear() {
    resetSearch();
    setResetSignal((previous) => previous + 1);
  }

  const showClear = hasSearched || jobs.length > 0 || status === "searching";

  return (
    <div className="shell">
      <header className="topbar">
        <span className="brand">RoleRadar</span>
        <span className={`status status-${status}`}>
          <span className="status-dot" />
          {STATUS_LABELS[status] ?? status}
        </span>
      </header>
      <div className="layout">
        <aside className="rail">
          <SearchBar onSearch={search} resetSignal={resetSignal} />
          <p className="rail-count">
            {jobs.length} match{jobs.length === 1 ? "" : "es"}
          </p>
          {showClear && (
            <button type="button" className="clear-button" onClick={handleClear}>
              Clear search
            </button>
          )}
        </aside>
        <main className="ledger">
          <JobList
            jobs={jobs}
            status={status}
            keywords={keywords}
            hasSearched={hasSearched}
            onSearch={search}
          />
        </main>
      </div>
    </div>
  );
}
