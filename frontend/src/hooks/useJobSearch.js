import { useCallback, useEffect, useRef, useState } from "react";

const WS_URL = "ws://localhost:8000/ws/jobs/search/";

export function useJobSearch() {
  const [jobs, setJobs] = useState([]);
  const [status, setStatus] = useState("connecting");
  const [keywords, setKeywords] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;

    socket.onopen = () => setStatus("idle");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.event === "search_started") {
        setJobs([]);
        setKeywords(data.keywords);
        setStatus("searching");
      }

      if (data.event === "job_match") {
        setJobs((previous) => [data.job, ...previous]);
      }

      if (data.event === "search_complete") {
        setStatus("idle");
        setHasSearched(true);
      }
    };

    socket.onclose = () => setStatus("disconnected");

    return () => socket.close();
  }, []);

  const search = useCallback((value) => {
    const socket = socketRef.current;
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ keywords: value }));
    }
  }, []);

  return { jobs, status, keywords, hasSearched, search };
}
