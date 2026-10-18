# Discord Bot Library 2.0  
全て自作したBotを作りたかったので，ライブラリを作りました．  
2.0なのは，以前作っていたものを1から作り直したからです．  
詳細の仕様については，[Overview](./docs/overview.md)を確認してください．  
  
## Develop  
開発は Python3.13 で行っています．  
  
## Sample code  
このサンプルコードでは，op:0(Dispatchイベント)にて「Ready」イベントを受信した際，指定されたチャンネルへ「Hello, World!」というメッセージを作成します．  
```python  
import os  
  
from discord_lib2.client import Bot  
from discord_lib2.logger import Logger  
from discord_lib2.event import GatewayEvent  
  
scriptPath = os.path.dirname(os.path.abspath(__file__))  
  
bot = Bot("your_bot_token")  
  
logger = Logger()  
logger.create_default_handler(os.path.join(scriptPath, "log"))  
  
class UserEvents(GatewayEvent):  
  async def ready(self, resources, ready_object):  
    from discord_lib2.objects.http_request.base.b_message import CreateMessage  
    message = CreateMessage(content="Hello, World!")  
    request_informations = resources.http_api.load_request(message, channel_id="channel_id(snowflake)")  
    await resources.http_api.request(request_informations)  
  
event = UserEvents()  
  
bot.boot(event, logger)  
```

## Feature
自身でこのライブラリを使用してBot開発を行っています．開発の際，ライブラリとして実装した方が良いと思った機能を段階的に実装していきます．  
また，余力があれば音声接続機能も実装しようと考えています．

## Dependencies  
### Library  
本ライブラリは，以下の Python ライブラリに依存しており，環境によっては追加インストールが必要になる場合があります．  
- aiohttp
- aioconsole
- dacite

## Hot to use
リポジトリをクローンし使用します．ライブラリ本体は`./discord_lib2`です．  
```shell
# リポジトリをクローンします
git clone https://github.com/dera-develop/Discord-lib-v2.git
cd ./Discord-lib-v2

# python実行環境を準備します
python -m venv myenv
# 以下OSに応じてどちらかを実行します
## Linux/MacOSで使用する場合
source ./myenv/bin/activate
## Windowsで使用する場合
cd ./myenv/Scripts && ./activate && ../..

# 外部ライブラリをインストールします
pip install aiohttp dacite

# 好きな名前のメインプログラムファイルを作成し実行します
python main.py
```

## Link  
- [Discord Developer Portal](https://discord.com/developers/applications)  
- [Discord API and SDK Reference](https://docs.discord.com/developers/reference)