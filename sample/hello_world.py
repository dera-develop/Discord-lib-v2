"""
READMEに掲載したものと同一のものです．
Gateway接続後，Readyイベントを受け取った際に指定されたチャンネルに
"Hello, World!"
と送信します．

以下の場所に，該当の物を設定します．
"your_bot_token"        : ボットトークン
"your_os"               : OS名（GatewayのIdentifyで使用します）
"channel_id(snowflake)" : 送信チャンネルID

ログは，このプログラムと同じ階層（./log/）へ保存されます．
ディレクトリが無い場合は，自動的に新しく作られます．
"""

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