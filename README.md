# 前提
現在このライブラリは **開発中** です．

### 実装済み
- Gateway接続
  - 接続の維持，イベントの送受信が可能
- HttpAPI
  - リクエストオブジェクトの定義（一部未実装）
  - リクエストの送信
    - Jsonフォーマットによるリクエスト送信
    - formフォーマットによるファイル送信
    （一部リクエストオブジェクトはファイル送信にまだ対応できていない可能性があります）
- Dispatchイベントをトリガーとするユーザー定義関数
- キャッシュ構造

### 開発中
- Dispatchイベントによるキャッシュ更新
- コマンド定義
  - Discordサーバーで使用できるコマンドの簡易定義のシステム
  - ターミナルで操作を行うための任意のコマンドを追加するためのシステム
- その他ライブラリの安定性・安全性の向上

#### 現在の実装処理
大々的にキャッシュ構造と更新処理を作り直しているため，現在のキャッシュ構造は将来的に使用できなくなります．

# Discord Bot Library 2.0
全て自作したBotを作りたかったので，ライブラリを作りました．
2.0なのは，以前作っていたものを1から作り直したからです．

このライブラリを使用することで，Discordサーバーとの通信の維持等の面倒な処理を意識せず，直観的にボットプログラムを作成することができます．
（最低限，どのフィールドにどの値を入れる必要があるのか等，公式ドキュメントの確認は必要です．）

## Develop version
開発は Python3.13 で行っています．

## Sample code
このサンプルコードでは，op:0(Dispatchイベント)にて「Ready」イベントを受信した際，指定されたチャンネルへ「Hello, World!」というメッセージを作成します．
```python
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
```

## Dependencies
### Library
本ライブラリは，以下の Python ライブラリに依存しており，環境によっては追加インストールが必要になる場合があります．

#### External Libraries
- websockets
- requests

#### Standart Libraries
- asyncio
- sys
- json
- zlib
- urllib
- logging
- dataclasses
- typing
- uuid

## Link
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API and SDK Reference](https://docs.discord.com/developers/reference)