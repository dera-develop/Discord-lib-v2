"""
READMEに掲載したものと同一のものです．
Gateway接続後，Readyイベントを受け取った際に指定されたチャンネルに
"Hello, World!"
と送信します．
"""

from discord_lib2.client import Bot
from discord_lib2.logger import Logger
from discord_lib2.event import GatewayEvent

bot = Bot("your_bot_token", "your_os")

logger = Logger()
logger.create_default_handler("log_dir_path")

class UserEvents(GatewayEvent):
  async def ready(self, resources, ready_object):
    from discord_lib2.objects.http_request.base.b_message import CreateMessage
    message = CreateMessage(content="Hello, World!")
    request_informations = resources.http_api.load_request(message, channel_id="channel_id(snowflake)")
    await resources.http_api.request(request_informations)

event = UserEvents()

bot.boot(event, logger)