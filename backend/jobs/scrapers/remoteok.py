import requests

from jobs.scrapers.base import BaseScraper


class RemoteOKScraper(BaseScraper):
    source_name = "remoteok"
    feed_url = "https://remoteok.com/api"

    def fetch_listings(self):
        response = requests.get(self.feed_url, headers={"User-Agent": "roleradar/1.0"})
        response.raise_for_status()
        entries = response.json()[1:]

        for entry in entries:
            yield {
                "title": entry.get("position", ""),
                "company": entry.get("company", ""),
                "location": entry.get("location", "remote"),
                "description": entry.get("description", ""),
                "url": entry.get("url", ""),
                "source": self.source_name,
            }
