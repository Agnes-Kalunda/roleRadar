from django.db import models
from pgvector.django import VectorField


class JobListing(models.Model):
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    source = models.CharField(max_length=100)
    source_url = models.URLField()
    dedupe_key = models.CharField(max_length=64, unique=True)
    embedding = VectorField(dimensions=384, null=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["dedupe_key"]),
            models.Index(fields=["source"]),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company}"


class SavedSearch(models.Model):
    owner_id = models.IntegerField()
    keywords = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keywords
