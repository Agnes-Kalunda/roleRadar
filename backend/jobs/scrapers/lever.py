import requests

from jobs.scrapers.base import BaseScraper


class LeverScraper(BaseScraper):
    def __init__(self, slug, company_name):
        self.slug = slug
        self.company_name = company_name
        self.source_name = f"lever:{slug}"

    def fetch_listings(self):
        url = f"https://api.lever.co/v0/postings/{self.slug}"
        response = requests.get(
            url,
            params={"mode": "json"},
            headers={"User-Agent": "roleradar/1.0"},
        )
        response.raise_for_status()
        entries = response.json()

        for entry in entries:
            categories = entry.get("categories", {})
            tags = [
                categories.get("team", ""),
                categories.get("department", ""),
                categories.get("commitment", ""),
            ]

            yield {
                "title": entry.get("text", ""),
                "company": self.company_name,
                "location": categories.get("location", ""),
                "description": entry.get("descriptionPlain", ""),
                "url": entry.get("hostedUrl", ""),
                "source": self.source_name,
                "tags": ",".join(tag for tag in tags if tag),
            }
