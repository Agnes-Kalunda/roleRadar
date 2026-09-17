from django.urls import re_path

from jobs.consumers import JobSearchConsumer

websocket_urlpatterns = [
    re_path(r"ws/jobs/search/$", JobSearchConsumer.as_asgi()),
]
