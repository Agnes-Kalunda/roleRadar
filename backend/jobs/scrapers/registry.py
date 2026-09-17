from jobs.scrapers.remoteok import RemoteOKScraper


def get_all_scrapers():
    return [
        RemoteOKScraper(),
    ]
