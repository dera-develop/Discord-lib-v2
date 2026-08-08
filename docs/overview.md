# OVERVIEW  
## 前提  
このライブラリは，GATEWAYイベントを使用したボットの作成を前提としたライブラリです．  
HTTPSリクエストのみを行うボットの作成には対応していません．  
（将来的には対応させるつもりです）  
  
## サンプルコード  
サンプルコード群は，[ここ](../sample/)に保存されています．  
ここでは，この中にある [hello_world.py](../sample/hello_world.py)をベースに解説を行います．  
```python  
# sample/hello_world.py  
  
from discord_lib2.client import Bot  
from discord_lib2.logger import Logger  
from discord_lib2.event import GatewayEvent  
  
bot = Bot("your_bot_token", "your_os")  
  
logger = Logger()  
logger.create_default_handler("log_dir_path")  
  
class UserEvents(GatewayEvent):  
  async def ready(self, resources, ready_object):  
    from discord_lib2.objects.http_request.body.b_message import CreateMessage  
    message = CreateMessage(content="Hello, World!")  
    request_informations = resources.http_api.load_request(message, channel_id="channel_id(snowflake)")  
    await resources.http_api.request(request_informations)  
  
event = UserEvents()  
  
bot.boot(event, logger)  
```  
  
## 使用するクラス等  
このライブラリを使用するために，最低以下の3つのクラスのimportが必要です．  
- discord_lib2/client.py [Botクラス](#Botクラス)  
- discord_lib2/logger.py [Loggerクラス](#Loggerクラス)  
- discord_lib2/event.py [GatewayEventクラス](#GatewayEventクラス)  
  
### Botクラス  
ボットを動かすためのメインになるクラスです．  
```python  
bot = Bot("your_bot_token", "your_os")  
```  
  
#### 引数  
- `bot_token` `str`  
ボットのトークンを設定します．  
このトークンは，Gateway接続の認証や，APIへのリクエストの認証に使用されます．  
- `os_type` `str`  
ボットを動作させるコンピューターのOSタイプを設定します．  
Gateway接続時の`Identify`イベントの送信で使用されます．  
  
#### インテントの設定  
Gatewayイベントを受信するための各種権限であるインテントの設定をこのBotクラスで行います．  
Botクラスのインスタンスを使い，起動前に設定を行います．  
インテントの項目は`bool`型で定義されており，値を`True`に変更することで自動的に値が計算され，`Identify`イベント時に送信されます．  
```python  
bot = Bot("your_bot_token", "your_os")  
  
bot.enable_guild_members = True  
bot.enable_message_content = True  
...  
```  
  
##### ⚠GUILDSインテントの扱いについて⚠  
全てのインテントはデフォルトで無効になっていますが，GUILDSインテントのみ，キャッシュの整合性を維持するため，値がデフォルトで`True`になっています．  
ここを`False`に意図的に変更してしまうと，キャッシュが破損し意図しない動作を行う可能性があります．  
  
#### 起動  
起動時は，以下のようにインスタンスのメゾッドを呼び出します．  
```python  
bot.boot(UserEventInstance, LoggerInstance)  
```  
UserEventInstanceとLoggerInstanceには，それぞれ後述する[Loggerクラス](#Loggerクラス)と[GatewayEventクラス](#GatewayEvent(ユーザーイベント)クラス)のインスタンスを渡します．  
  
### Loggerクラス  
ターミナルやファイルへのログ出力を管理するクラスです．`Logging`ライブラリをベースに作成しています．  
`Loggint`ライブラリに対応する形であれば，ユーザーが自由にログの出力先や出力レベルを設定できます．  
  
#### ユーザー設定  
ユーザー自身で設定を行う際は，`Logger`クラス内の`logger`変数が，Loggingの親に設定されているので，そこへハンドラを追加してください．最小レベルは`Debug`になっています．  
```python  
Logger = Logger()  
Logger.logger # loggingの親変数 ここに設定していく  
```  
  
##### ⚠注意⚠  
Discord_Lib2.0では，`asyncio`を使用した非同期処理を使用し構築されています．  
そのため，ユーザー自身で設定を行う際は，それに対応させた形でのログ出力を行う必要があります．  
  
#### デフォルト設定  
もし設定が面倒である場合は，ログ出力の設定関数を用意してあるので，それを利用することができます．  
```python  
Logger = Logger()  
logger.create_default_handler("log_dir_path")  
```  
`log_directory` `str(PATH)`  
ログを出力するディレクトリの絶対パスを指定します．対象のディレクトリが存在しなかった場合は，自動的に作成されます．  
  
このデフォルト関数では，ターミナルとファイルにログが出力されます．  
ターミナルには，`Debug`レベル以上のログが，ファイルには`Info`レベル以上のログが出力されます．  
ファイルは，関数の引数で指定されたディレクトリ内に，以下のフォーマットに従った名前で作成されます．  
```  
# log file name  
logYYYYmmdd_HHMMSS.log  
```  
作成したLoggerインスタンスは，ボットの起動メゾッドを呼び出す際，引数として渡す必要があります．  
  
### GatewayEventクラス  
Gateway接続を通じて受信されるイベントの中の，`DISPATCH (OP:0)`イベントの受信をトリガーとして実行できる，ユーザー関数を定義することができます．  
```python  
class UserEvents(GatewayEvent):  
  async def ready(self, resources, ready_object):  
    ...  
  
  async def message_create(self, resources, message_create_object):  
    ...  
```  
関数や変数を定義する際は，以下の項目を守る必要があります．  
- GatewayEventクラスをオーバーライドしたクラスを作成し，その中で関数定義の再定義を行います．  
- 関数は全て`async def`を使用した宣言を行う必要があります．  
  
各関数には，必ず`self` と `resources` が設定されており，追加でほぼすべてのイベント関数に各イベントの受信データに対応したイベントオブジェクトが設定されています．  
- [resources](#resources)  
- [イベントオブジェクト](#event_object)  
  
#### resources  
これには，ギルドやユーザーのキャッシュ，HTTPリクエスト関数，Gatewayリクエスト関数，ロガーが含まれています．  
```  
resources  
 ├─ cache  
 │   ├─ data  
 │   │   ├─ guilds  
 │   │   │   └─ # Guildペイロードをベースとしたデータクラス  
 │   │   └─ users  
 │   │       ├─ user  
 │   │       │   └─ # Userペイロードをベースとしたデータクラス  
 │   │       └─ joined_guilds  
 │   │           └─ # 参加しているギルドのリスト  
 │   └─ additional  
 │　　　　└─　# ユーザーが自由に使用できる辞書型変数  
 │  
 ├─ http_api  
 │   ├─ load_request # リクエスト情報の生成関数  
 │   └─ request      # リクエスト関数  
 │  
 ├─ gateway  
 │   ├─ request_guild_member       # ギルドメンバーのリクエスト関数  
 │   ├─ request_soundboard_sounds  # サウンドボードのリクエスト関数  
 │   └─ request_channel_info       # チャンネル情報のリクエスト関数  
 │  
 └─ logger # loggingを使用したロガー  
```  
  
##### キャッシュ  
キャッシュは，各`DISPATCH`イベントに応じて自動的に更新されます．  
  
###### data  
自動更新されるキャッシュ構造です．変数として定義してあるため，メゾッドとして内部のほぼすべてのキャッシュデータを簡単に呼び出せます．  
  
###### data/guilds  
ボットが参加しているギルドの情報を，各ギルドのIDをキーとした辞書型で保存します．  
```python  
resources.data.guilds["guild_id"] # -> guild cache object  
  
resources.data.guilds["guild_id"].name # -> guild name  
resources.data.guilds["guild_id"].channels["channel_id"].name # -> channel name  
```  
`DISPATCH`イベントの`GUILD_CREATE`イベントのデータ構造をベースにキャッシュの構造を構築しています．リスト型で送られてくるものは，`user_id`や`guild_id`等ユニークキーで判別可能なものは，それをキーとした辞書型に変換した後キャッシュ保存を行っています．  
構造の詳細は，[Guildsキャッシュソースコード](../discord_lib2/cache/user/guild.py)や[Discord公式ドキュメント[Guild Createイベント]](https://docs.discord.com/developers/events/gateway-events#guild-create)を確認してください．  
  
###### data/users  
ボットが参加しているギルドに所属しているユーザーの情報を，各ユーザーのIDをキーとした辞書型で保存します．  
```python  
resources.cache.data.users["user_id"] # -> user cache object  
  
resources.cache.data.users["user_id"].bot # -> bot flag  
resources.cache.data.users["user_id"].global_name # -> user global name  
```  
`DISPATCH`イベントの`USER_UPDATE`や，その他ギルドメンバーの情報を受け取るイベントが発生した際に更新されます．  
キャッシュの構造は，Userペイロードです．構造の詳細は，[Usersキャッシュソースコード](../discord_lib2/cache/user/user.py)や[Discord公式ドキュメント[Userオブジェクト]](https://docs.discord.com/developers/resources/user#user-object)を確認してください．  
  
###### additional  
ユーザーが自由に使用できる，辞書型の変数です．  
自動処理で一切触れられることはない為，ユーザーが自由にキャッシュ構造を構築できます．  
  
##### HttpAPI  
APIへのリクエストを行う際に使用する関数が定義されています．  
各リクエストボディーやクエリ，リクエスト先については，[公式ドキュメント[APIリファレンス]](https://docs.discord.com/developers/reference)を確認してください．  
  
リクエストは，以下の手順を踏み行います．  
1. リクエストボディーの作成  
リクエストボディーを作成します．リクエストボディーのほとんどは定義されており，`discord_lib2/objects/http_request/body/b_*.py`に定義されています．必要に応じてimportし使用します．また，各クラスは`dataclasses`ライブラリの`dataclass`を使用しています．  
2. クエリの作成  
リクエストに必要な場合（特にGetリクエスト等）は，クエリを作成します．クエリもほとんどが定義されており，`discord_lib2/objects/http_request/request_query/q_*.py`に定義されています．こちらも必要に応じてimportし使用します．こちらも各クラスが`dataclasses`ライブラリの`dataclass`を使用しています．  
3. リクエスト情報の生成  
`http_api.load_request`関数を使用し，リクエスト情報を生成します．戻り値は`RequestInfomation`です．  
・`request_object` リクエストボディーを設定します．  
・`request_query_object` リクエストクエリを設定します．  
・`*_id` リクエストの送信先に含める必要のある各種ID等を指定します．  
必要な`*_id`が指定されていない場合は，生成時に例外が発生します．  
4. リクエストの送信  
`http_api.request`関数を使用し，リクエストを送信します．戻り値は`requests.Responce`です．  
引数に **3** で作成した`RequestInfomation`をそのまま渡します．  
  
###### サンプルコード  
```python  
  # Get reaction request  
  
async def dispatch_event_function(self, resources, ...):  
  from discord_lib2.objects.http_request.body import b_message  
  from discord_lib2.objects.http_request.request_query import q_message  
  
  reactions = b_message.GetReactions()                        # request_body  
  reactions_query = q_message.GetReactions(type=0, limit=20)  # request_query  
  request_informations = resources.http_api.load_request(reactions, reactions_query, channel_id="0123456789", message_id="0123456789", emoji_id="0123456789")  
  await resources.http_api.request(request_informations)      # request  
```  
```python  
  # No query  
  # Create message request  
  
async def dispatch_event_function(self, resources, ...):  
  from discord_lib2.objects.http_request.body.b_message import CreateMessage  
  
  message = CreateMessage(content="Hello, World!")          # request_body  
  request_informations = resources.http_api.load_request(message, channel_id="0123456789")  
  await resources.http_api.request(request_informations)    # request  
```  
  
##### gateway  
Gateway接続を通じて送信するリクエストを送信します．  
送信前に，リクエストボディーを作成する必要があり，`discord_lib2/objects/gateway/request_payload.py`に定義されています．  
各クラスは`dataclasses`ライブラリの`dataclass`を使用しています．  
  
###### request_guild_member  
⚠キャッシュの更新処理等で自動的に呼ばれるため，意図的に呼ぶ必要はあまりありません⚠  
ギルドメンバーのリクエストを送信します．  
使用するクラスは，`RequestGuildMembers`クラスです．  
```python  
from discord_lib2.objects.gateway import request_payload  
request_data = request_payload.RequestGuildMembers("guild_id", 0, "", True)  
await gateway.request_guild_member(request_data)  
```  
  
###### request_soundboard_sounds  
ギルドのサウンドボードのリクエストを送信します．  
使用するクラスは，`RequestSoundboardSounds`クラスです．  
```python  
from discord_lib2.objects.gateway import request_payload  
request_data = request_payload.RequestSoundboardSounds(["guild_id1", "guild_id2"])  
await gateway.request_soundboard_sounds(request_data)  
```  
  
###### request_channel_info  
ギルドのチャンネル情報のリクエストを送信します．  
使用するクラスは，`RequestChannelInfo`クラスです．  
```python  
from discord_lib2.objects.gateway import request_payload  
request_data = request_payload.RequestChannelInfo("guild_id", ["fiels1", "field2"])  
await gateway.request_channel_info(request_data)  
```  
  
##### ロガー  
LoggingのLoggerが設定されています．冒頭のBotインスタンスに渡したLoggerを親として，`GUE(Gateway User Event)`という名前でログが出力されます．  
```python  
resources.logger.info(...)  
resources.logger.error(...)  
```  
  
#### event_object  
各受信イベントに対応したデータ構造が定義されています．定義の有無は，[ユーザーイベントソースコード](../discord_lib2/event.py)を確認してください．  
定義されている場合は，そのイベントで受信したデータを，受信した構造をそのままに，インスタンス変数を呼び出す感覚で取得することができます．  
```python  
async def message_create(self, resources, message_create_object):  
  message_create_object.content # -> message content  
  message_create_object.member.nick # -> message creator nick  
```  
部分更新イベントなどが発生した場合，値が存在しない場合は`None`になるため，ユーザーは型エラー等が起きないように型チェック等を行う必要があります．  
各イベントの受信データ構造については，[Discord公式ドキュメント[Gatewayイベント]](https://docs.discord.com/developers/events/gateway-events)を参照してください．