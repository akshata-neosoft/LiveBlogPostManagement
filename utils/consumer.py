import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BlogPostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'live_blogs'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Usually you don't handle receiving on client -> server side in this use case
        pass

    async def blog_post_event(self, event):
        await self.send(text_data=json.dumps(event['data']))
