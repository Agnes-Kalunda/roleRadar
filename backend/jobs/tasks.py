import hashlib

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from sentence_transformers import SentenceTransformer

from jobs.models import JobListing
from jobs.scrapers.registry import get_all_scrapers

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    return _model


def make_dedupe_key(title, company, location):
    raw = f"{title.lower()}|{company.lower()}|{location.lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()


@shared_task
def run_all_scrapers():
    for scraper in get_all_scrapers():
        scrape_source.delay(scraper.source_name)


@shared_task
def scrape_source(source_name):
    scraper = next(s for s in get_all_scrapers() if s.source_name == source_name)
    for raw_job in scraper.fetch_listings():
        process_scraped_job.delay(raw_job)


@shared_task
def process_scraped_job(raw_job):
    dedupe_key = make_dedupe_key(
        raw_job["title"], raw_job["company"], raw_job.get("location", "")
    )
    if JobListing.objects.filter(dedupe_key=dedupe_key).exists():
        return

    embedding = get_embedding_model().encode(raw_job["description"]).tolist()

    job = JobListing.objects.create(
        title=raw_job["title"],
        company=raw_job["company"],
        location=raw_job.get("location", ""),
        description=raw_job["description"],
        source=raw_job["source"],
        source_url=raw_job["url"],
        dedupe_key=dedupe_key,
        embedding=embedding,
    )
    broadcast_new_job(job)


def broadcast_new_job(job):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "search_broadcast",
        {
            "type": "job.match",
            "job": {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.source_url,
            },
        },
    )
