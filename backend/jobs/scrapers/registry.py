from jobs.scrapers.remoteok import RemoteOKScraper
from jobs.scrapers.jobicy import JobicyScraper
from jobs.scrapers.weworkremotely import WeWorkRemotelyScraper
from jobs.scrapers.greenhouse import GreenhouseScraper
from jobs.scrapers.lever import LeverScraper
from jobs.scrapers.companies import GREENHOUSE_COMPANIES, LEVER_COMPANIES


def get_all_scrapers():
    scrapers = [
        RemoteOKScraper(),
        JobicyScraper(),
        WeWorkRemotelyScraper(),
    ]

    for company in GREENHOUSE_COMPANIES:
        scrapers.append(GreenhouseScraper(company["slug"], company["name"]))

    for company in LEVER_COMPANIES:
        scrapers.append(LeverScraper(company["slug"], company["name"]))

    return scrapers
