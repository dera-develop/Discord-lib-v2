# GATEWAY EVENT
`Gateway`接続で受信するイベントの，`op:0`, `DISPATCH`イベントをトリガーとし，ユーザーの任意処理を実行できます．

使用するクラスは，`discord_lib2.event`の`GatewayEvent`です．
ボットを作成する際，このクラスをオーバーライドし使用します．

### Example
```python
from discord_lib2.event import GatewayEvent

class UserEvent(GatewayEvent):
  async def ready(self, resources, ready_object):
    ...

user_event = UserEvent()

bot.boot(..., event=user_event)
```

各イベントは，`GatewayEvent`にほとんどが宣言されており，各イベントの詳細は，[Discord公式ドキュメント #Received Events](https://docs.discord.com/developers/events/gateway-events#receive-events)に記載されています．
クラス内ではここで記述されているイベント名で宣言されています．
また，このクラス内には`gateway_close_event`というイベント関数が定義されています．
この関数については，後述の[Gateway終了イベント](#gateway終了イベント)を参照してください．

### 引数
各イベントには，必ず`resources`が定義されており，部分的に各イベントの受信データオブジェクトが定義されています．
`self`と`resources`以外の引数要素が受信データオブジェクトです．
```python
class GatewayEvent:
  async def ready(self, resources, ready_object):   # ready_object: 受信データオブジェクト
    pass
  ...

  async def message_create(self, resources, message_create_object): # message_create_object: 受信データオブジェクト
    pass
  ...
```

#### resources
ライブラリ内のオブジェクトとやり取りする物です．
Gateway接続関係，APIリクエスト，キャッシュの操作はこの変数を通じて行う必要があります．
以下は，この引数の構造です．
```
resources
 ├─ cache
 │   ├─ application # applicationオブジェクト
 │   │   
 │   ├─ data
 │   │   ├─ guilds
 │   │   │   └─ # GuildCreateイベント構造をベースとしたデータクラス
 │   │   └─ users
 │   │       ├─ user
 │   │       │   └─ # User構造をベースとしたデータクラス
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
 ├─ logger    # loggingを使用したロガー
 │
 └─ bot_stop  # botを停止させる関数

```

##### cache
キャッシュは，各`DISPATCH`イベントに応じて自動的に更新されます．

###### application
アプリケーションオブジェクトです．`GetCurrentApplication`ポイントを使用して取得した，ボットのアプリケーション情報を格納しています．

###### data
自動更新されるキャッシュ構造です．変数として定義してあるため，メゾッドとして内部のほぼすべてのキャッシュデータを簡単に呼び出せます．

###### data/guilds
ボットが参加しているギルドの情報を，各ギルドのIDをキーとした辞書型で保存します．
```python
resources.cache.data.guilds["guild_id"] # -> guild cache object

resources.cache.data.guilds["guild_id"].name # -> guild name
resources.cache.data.guilds["guild_id"].channels["channel_id"].name # -> channel name
```
`DISPATCH`イベントの`GUILD_CREATE`イベントのデータ構造をベースにキャッシュの構造を構築しています．リスト型で送られてくるものは，`user_id`や`guild_id`等ユニークキーで判別可能なものは，それをキーとした辞書型に変換した後キャッシュ保存を行っています．
構造の詳細は，[Guildsキャッシュソースコード](../discord_lib2/cache/user/guild.py)や[Discord公式ドキュメント[Guild Createイベント]](https://docs.discord.com/developers/events/gateway-events#guild-create)を確認してください．

###### data/users
ボットが参加しているギルドに所属しているユーザーの情報を，各ユーザーのIDをキーとした辞書型で保存します．
```python
resources.cache.data.users["user_id"] # -> user cache object

resources.cache.data.users["user_id"].user.bot # -> bot flag
resources.cache.data.users["user_id"].user.global_name # -> user global name
```
`DISPATCH`イベントの`USER_UPDATE`や，その他ギルドメンバーの情報を受け取るイベントが発生した際に更新されます．
`data.users.joined_guilds`には，ユーザーが参加中かつボットが参加しているギルドのIDがリスト型で格納されます．
`data.users.user`のキャッシュ構造はUser構造です．構造の詳細は，[Usersキャッシュソースコード](../discord_lib2/cache/user/user.py)や[Discord公式ドキュメント[Userオブジェクト]](https://docs.discord.com/developers/resources/user#user-object)を確認してください．

###### additional
ユーザーが自由に使用できる変数です．
自動処理で一切触れられることはない為，ユーザーが自由にキャッシュ構造を構築できます．
型ヒントに`Any`型を付けてあるように，どのような型でも自由に使うことができます．
デフォルトでは空の`dict`変数として宣言しているので，他の型で使う場合は，上書きで宣言をする必要があります．

##### HttpAPI
APIへのリクエストを行う際に使用する関数が定義されています．  
詳細は，[HTTP API](http_api.md)ドキュメントを参照してください．  
`load_request`と`request`はそれぞれ，ドキュメントの[リクエスト情報の作成セクション](http_api.md#リクエスト情報の作成)と[リクエストの送信セクション](http_api.md#リクエストの送信)です．


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
await resources.gateway.request_guild_member(request_data)
```

###### request_soundboard_sounds
ギルドのサウンドボードのリクエストを送信します．
使用するクラスは，`RequestSoundboardSounds`クラスです．
```python
from discord_lib2.objects.gateway import request_payload
request_data = request_payload.RequestSoundboardSounds(["guild_id1", "guild_id2"])
await resources.gateway.request_soundboard_sounds(request_data)
```

###### request_channel_info
ギルドのチャンネル情報のリクエストを送信します．
使用するクラスは，`RequestChannelInfo`クラスです．
```python
from discord_lib2.objects.gateway import request_payload
request_data = request_payload.RequestChannelInfo("guild_id", ["fiels1", "field2"])
await resources.gateway.request_channel_info(request_data)
```

##### logger
LoggingのLoggerが設定されています．冒頭のBotインスタンスに渡したLoggerを親として，`UserEvent`という名前でログが出力されます．
```python
resources.logger.info(...)
resources.logger.error(...)
```

##### bot_stop
Botを停止させる関数です．  
非同期関数のため，実行するには`await`する必要があります．
**注意**
この関数で実行が終了するのではなく，ライブラリ内部にあるキューに停止命令を追加する関数のため，キューから値が取得されるまで処理は継続されます．

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

### Gateway終了イベント
`gateway_close_event`クラスは，内部で`Gateway`接続が終了する際に実行されるイベント関数です．
（これには，再接続のための切断，異常終了による切断，実行終了時の切断が含まれます）