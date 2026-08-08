'''
Gateway接続後，Readyイベントを受け取った際に指定されたチャンネルにファイルを送信します．

ファイルは，通常のリクエストオブジェクトの内容定義と異なり，オブジェクトに追加する形です．
'''

from discord_lib2.client import Bot
from discord_lib2.logger import Logger
from discord_lib2.event import GatewayEvent

bot = Bot("bot_token", "os_type")

logger = Logger()
logger.create_default_handler("log_dir_path")

class user_events(GatewayEvent):
  async def ready(self, resources, ready_object):
    from discord_lib2.objects.http_request.body import b_message
    message = b_message.CreateMessage(content="Ready image")
    await message.files.add_file("picture_file_path")
    message.attachments = [b_message.AttachmentRequest(id=0, filename="picture_name")]
    request = resources.http_api.load_request(message, channel_id="send_channel_id")
    await resources.http_api.request(request)

event = user_events()

bot.boot(event, logger)