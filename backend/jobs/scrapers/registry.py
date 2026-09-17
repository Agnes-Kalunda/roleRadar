from jobs.scrapers.remoteok import RemoteOKScraper
from jobs.scrapers.jobicy import JobicyScraper
from jobs.scrapers.weworkremotely import WeWorkRemotelyScraper


def get_all_scrapers():
    return [
        RemoteOKScraper(),
        JobicyScraper(),
        WeWorkRemotelyScraper(),
    ]
