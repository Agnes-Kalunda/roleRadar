import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [value, setValue] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (value.trim()) {
      onSearch(value.trim());
    }
  }

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <label htmlFor="keywords">Keywords</label>
      <input
        id="keywords"
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="frontend developer, remote"
      />
      <button type="submit">Search</button>
    </form>
  );
}
