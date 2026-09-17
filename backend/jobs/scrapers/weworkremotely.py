import re

import requests
from xml.etree import ElementTree

from jobs.scrapers.base import BaseScraper


class WeWorkRemotelyScraper(BaseScraper):
    source_name = "weworkremotely"
    feed_url = "https://weworkremotely.com/remote-jobs.rss"

    def fetch_listings(self):
        response = requests.get(self.feed_url, headers={"User-Agent": "roleradar/1.0"})
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)

        for item in root.findall(".//item"):
            raw_title = item.findtext("title", "")
            company, _, title = raw_title.partition(": ")
            if not title:
                title = company
                company = ""

            raw_description = item.findtext("description", "")
            description = re.sub(r"<[^<]+?>", "", raw_description).strip()

            tags = [
                category.text
                for category in item.findall("category")
                if category.text
            ]

            yield {
                "title": title,
                "company": company,
                "location": "Remote",
                "description": description,
                "url": item.findtext("link", ""),
                "source": self.source_name,
                "tags": ",".join(tags),
            }
