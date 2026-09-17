import json

from channels.generic.websocket import AsyncWebsocketConsumer


class JobSearchConsumer(AsyncWebsocketConsumer):
    group_name = "search_broadcast"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        keywords = data.get("keywords", "")
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "search.started",
                "keywords": keywords,
            },
        )

    async def search_started(self, event):
        await self.send(text_data=json.dumps({
            "event": "search_started",
            "keywords": event["keywords"],
        }))

    async def job_match(self, event):
        await self.send(text_data=json.dumps({
            "event": "job_match",
            "job": event["job"],
        }))
