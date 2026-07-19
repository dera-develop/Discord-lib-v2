import os

from discord_lib2.client import Bot
from discord_lib2.logger import Logger

from discord_lib2.event import GatewayEvent
from discord_lib2.objects.resources import UserEventResources

scriptPath = os.path.dirname(os.path.abspath(__file__))

bot = Bot("your_bot_token", "your_os")

logger = Logger()
logger.create_default_handler(os.path.join(scriptPath, "log"))

class UserEvents(GatewayEvent):
  async def ready(self, resources: UserEventResources):
    from discord_lib2.objects.http_request.base.b_message import CreateMessage
    message = CreateMessage(content="Hello, World!")
    request_informations = resources.http_api.load_request(message, channel_id="channel_id(snowflake)")
    await resources.http_api.request(request_informations)

event = UserEvents()

bot.boot(event, logger)