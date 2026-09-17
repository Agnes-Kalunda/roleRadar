import requests

from jobs.scrapers.base import BaseScraper


class JobicyScraper(BaseScraper):
    source_name = "jobicy"
    feed_url = "https://jobicy.com/api/v2/remote-jobs"

    def fetch_listings(self):
        response = requests.get(
            self.feed_url,
            params={"count": 100},
            headers={"User-Agent": "roleradar/1.0"},
        )
        response.raise_for_status()
        entries = response.json().get("jobs", [])

        for entry in entries:
            tags = entry.get("jobIndustry", []) + entry.get("jobType", [])
            yield {
                "title": entry.get("jobTitle", ""),
                "company": entry.get("companyName", ""),
                "location": entry.get("jobGeo", ""),
                "description": entry.get("jobExcerpt", ""),
                "url": entry.get("url", ""),
                "source": self.source_name,
                "tags": ",".join(tags),
            }
