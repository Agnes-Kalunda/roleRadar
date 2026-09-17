class BaseScraper:
    source_name = "base"

    def fetch_listings(self):
        raise NotImplementedError
