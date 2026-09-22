import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from jobs.models import JobListing


class JobSearchConsumer(AsyncWebsocketConsumer):
    group_name = "search_broadcast"

    async def connect(self):
        self.keywords = ""
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        keywords = data.get("keywords", "").strip()
        self.keywords = keywords

        await self.send(text_data=json.dumps({
            "event": "search_started",
            "keywords": keywords,
        }))

        for job in await self.find_existing_matches(keywords):
            await self.send(text_data=json.dumps({
                "event": "job_match",
                "job": job,
            }))

        await self.send(text_data=json.dumps({"event": "search_complete"}))

        from jobs.tasks import run_all_scrapers
        await sync_to_async(run_all_scrapers.delay)()

    @database_sync_to_async
    def find_existing_matches(self, keywords):
        query = Q(title__icontains=keywords) | Q(company__icontains=keywords) | Q(tags__icontains=keywords)
        jobs = JobListing.objects.filter(query).order_by("-scraped_at")[:50]
        return [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.source_url,
                "tags": job.tags,
                "scraped_at": job.scraped_at.isoformat(),
            }
            for job in jobs
        ]

    def matches_keywords(self, job):
        if not self.keywords:
            return False
        haystack = f"{job['title']} {job['company']} {job['location']}".lower()
        return self.keywords.lower() in haystack

    async def job_match(self, event):
        if self.matches_keywords(event["job"]):
            await self.send(text_data=json.dumps({
                "event": "job_match",
                "job": event["job"],
            }))
