import re

import requests

from jobs.scrapers.base import BaseScraper


class GreenhouseScraper(BaseScraper):
    def __init__(self, slug, company_name):
        self.slug = slug
        self.company_name = company_name
        self.source_name = f"greenhouse:{slug}"

    def fetch_listings(self):
        url = f"https://boards-api.greenhouse.io/v1/boards/{self.slug}/jobs"
        response = requests.get(
            url,
            params={"content": "true"},
            headers={"User-Agent": "roleradar/1.0"},
        )
        response.raise_for_status()
        entries = response.json().get("jobs", [])

        for entry in entries:
            location = entry.get("location", {}).get("name", "")
            raw_description = entry.get("content", "")
            description = re.sub(r"<[^<]+?>", "", raw_description).strip()
            departments = [
                department.get("name", "")
                for department in entry.get("departments", [])
            ]

            yield {
                "title": entry.get("title", ""),
                "company": self.company_name,
                "location": location,
                "description": description,
                "url": entry.get("absolute_url", ""),
                "source": self.source_name,
                "tags": ",".join(departments),
            }
