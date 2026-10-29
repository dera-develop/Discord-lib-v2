# HTTP API
DiscordのHttpAPIへのリクエストに関するドキュメントです．

## 概要
### システム
リクエストには，`aiohttp`ライブラリを使用した非同期リクエストを使用しています．
HttpAPIリクエストは，`asyncio.create_task()`を使用して作られた単一タスクでリクエスト処理が行われます．

### リクエストの作成
リクエストの作成と送信は，以下の流れで行われます．

1. **リクエストオブジェクトの作成** [(詳細)](#リクエストオブジェクトの作成)
  リクエストオブジェクトを作成します．  
  リクエストオブジェクトは`dataclass`を使用してクラス定義されており，該当クラスのインスタンスを作成することで作成することができます．  
  定義の詳細は，[リクエストオブジェクトの詳細]()を参照してください．

2. **クエリオブジェクトの作成** [(詳細)](#クエリオブジェクトの作成)
  リクエストに必要なクエリオブジェクトを作成します．  
  リクエストオブジェクトと同じく`dataclass`を使用してクラス定義がされています．
  クエリは各オプションに必ず存在するわけではなく，存在していても定義が任意である可能性があります．  
  定義が必須ではない場合は，この手順をスキップすることができます．
  定義の詳細は，[リクエストオブジェクトの詳細]()の各リクエスト内容に記述されています．

3. **リクエスト情報の作成** [(詳細)](#リクエスト情報の作成)
  専用関数を使用し，リクエスト情報を作成します．  
  リクエスト情報の生成関数は，[ゲートウェイイベント](../gateway_event.md)関数，[アプリケーションコマンド](../applicarion_commands.md)関数，[ターミナルコマンド](../user_terminal_commands.md)関数で呼び出すことができます．
  定義位置は，各ドキュメントを参照してください．

4. **リクエストの送信** [(詳細)](#リクエストの送信)
  *手順3* で作成したリクエスト情報を使用し，リクエストを送信します．

*1と2は順不同です．
  
## リクエスト手順の詳細
### リクエストオブジェクトの作成
リクエストオブジェクトは，`discord_lib2/objects/http_request/body/*`へファイルごとに定義されています．必要に応じてファイルをインポートし使用します．  
各ファイルは，`b_*.py`という名前で定義されています．`b_`は`body_`の略称であり，クエリオブジェクトとの競合を避けるために付与されています．  
  
各リクエストオブジェクトは，[公式ドキュメント "APIリファレンス"](https://docs.discord.com/developers/reference)に記述されているリクエストボディーの名称と型を基準に`dataclass`を使用して定義されています．
```python
# Create Message object
# discord_lib2/objects/http_request/body/b_message/CreateMessage
@dataclass
class CreateMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages"
  req_type: ClassVar[str] = "post"

  content: str | Exclude = Exclude()
  nonce: int | str | Exclude = Exclude()
  tts: bool | Exclude = Exclude()
  embeds: list[Embed] | Exclude = Exclude()
  allowed_mentions: AllowedMentions | Exclude = Exclude()
  message_reference: MessageReference | Exclude = Exclude()
  components: list[component.ComponentClass] | Exclude = Exclude()
  sticker_ids: list[snowflake] | Exclude = Exclude()
  files: FormFile = field(default_factory=FormFile)
  payload_json: str | Exclude = Exclude()
  attachments: list[AttachmentRequest] | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  enforce_nonce: bool | Exclude = Exclude()
  poll: ShardClientTheme | Exclude = Exclude()
```
各クラスには，`req_url`と`req_type`，リクエストボディーの値が定義されています．  
`req_url`と`req_type`は，リクエスト情報の生成時にリクエスト先とリクエストタイプの設定に使用されます．  
リクエストボディーの項目の詳細については，Discord公式ドキュメントを参照してください．  

#### Excludeクラスについて
`Exclude`クラスは，名前の通り除外を行うためのクラスです．デフォルトでこのクラスが定義されている場合は，その値はリクエストに必須ではないということです．
> **必須ではない**と**Noneの許容**は別物であり，`Exclude`クラスが設定されていないものは，`None`でも定義を行う必要があります．

#### snowflake変数型について
変数型`snowflake`は，`str`型と同一です．

#### ファイルの送信について
このライブラリでは，ファイルをフォームデータとして送信することも可能です．  
> このライブラリには，ファイル送信引数として定義されていないリクエストオブジェクトが存在する可能性があります．

上記の`CreateMessage`オブジェクトもそのひとつです．  
ファイル送信を行えるクラスは，`FormFile`クラスとして定義されています．
```python
# Create Message object
# 
@dataclass
class CreateMessage(__MessageBase):
  ...
  files: FormFile = field(default_factory=FormFile)
  ...
```
ファイルを追加するには，`FormFile`インスタンスにある`add_file`メゾッドを使用します．
```python
async def add_file(self, file_path: str) -> None
```
- **file_path `String`**
  送信したいファイルの絶対パスを指定します．

この関数内では，ファイル名とファイルタイプの取得，ファイルのバイナリデータの取得を行い，リクエストボディーへ登録します．  
ファイルは「追加」されていくので，複数回実行することで複数ファイルを登録することができます．
##### Example
```python
message_object = CreateMessage(   # create instance
  content="image example"
)
message_object.add_file("send/file_0/path") # add file
message_object.add_file("send/file_1/path") # add file
```

---

### クエリオブジェクトの作成
クエリオブジェクトは，リクエストオブジェクト同様に定義されており，同一の制約で使用することができます．  
定義ファイルの場所は，`discord_lib2/objects/http_request/query/*`で，`q_*.py`と定義されている物です．  
使用するクエリのクラス名は，リクエストオブジェクトで使用するクラス名と同一の名前の物を使用します．
```python
# Get Reaction query
# discord_lib2/objects/http_request/query/q_message/GetReactions
@dataclass
class GetReactions(BaseClass):
  type: int | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()
```

---

### リクエスト情報の作成
リクエストを行う際，リクエスト情報オブジェクトを作成する必要があります．  
リクエスト情報の生成関数は，[ゲートウェイイベント](../gateway_event.md)の各イベント関数，[アプリケーションコマンド](../applicarion_commands.md)の実行関数，[ターミナルコマンド](../user_terminal_commands.md)の実行関数で呼び出すことができます．  
各関数内での定義位置は，各ドキュメントを参照してください．

#### 関数の使い方
関数は，以下の様に定義されています．
```python
def load_request(
    self,
    request_object: body_base.BaseClass,
    request_query_object: query_base.BaseClass | None = None,
    application_id: str | None=None,
    instance_id: str | None=None,
    guild_id: str | None=None,
    auto_moderation_rule_id: str | None=None,
    channel_id: str | None=None,
    overwrite_id: str | None=None,
    user_id: str | None=None,
    message_id: str | None=None,
    emoji_id: str | None=None,
    entitlement_id: str | None=None,
    guild_scheduled_event_id: str | None=None,
    template_code: str | None=None,
    role_id: str | None=None,
    integration_id: str | None=None,
    interaction_id: str | None=None,
    interaction_token: str | None=None,
    invite_code: str | None=None,
    lobby_id: str | None=None,
    answer_id: str | None=None,
    sound_id: str | None=None,
    sticker_id: str | None=None,
    pack_id: str | None=None,
    sku_id: str | None=None,
    subscription_id: str | None=None,
    webhook_id: str | None=None,
    webhook_token: str | None=None,
    command_id: str | None=None) -> RequestInformation
```
- **request_object `body_base.BaseClass`**
  リクエストオブジェクトのインスタンスを渡します．`body_base.BaseClass`は，各リクエストオブジェクトクラスの親クラスです．
- **request_query_object `query_base.BaseClass`**
  リクエストクエリのインスタンスを渡します．`query_base.BaseClass`は，各リクエストクエリクラスの親クラスです
- **以降の引数**
  以降の引数は，全てURL生成時に渡す引数です．  
  DiscordのHttpAPIのURLでは，リクエストに応じて各種IDやトークンを必要とします．    
  必要な引数の詳細は，各リクエストオブジェクトの詳細を参照してください．
  ```python
  # Get Reactions
  from discord_lib2.objects.http_request.body import b_message
  from discord_lib2.objects.http_request.request_query import q_message

  reactions = b_message.GetReactions()          # request_body
  reactions_query = q_message.GetReactions(     # request_query
    type=0,
    limit=20
  )
  request_information = load_request(   # create request informations
    reactions,
    reactions_query,
    channel_id="0123456789",
    message_id="0123456789",
    emoji_id="0123456789"
  )
  ```
  ```python
  # No query
  # Create Message
  from discord_lib2.objects.http_request.body.b_message import CreateMessage

  message = CreateMessage(    # request_body
    content="Hello, World!"
  )
  request_information = load_request(
    message,
    channel_id="0123456789"
  )
  ```

---

### リクエストの送信
リクエスト情報オブジェクトを作成したら，リクエストを送信します．  
リクエスト送信関数は，リクエスト情報生成関数と同じ場所で使用できます．

#### 関数の使い方
関数は，以下の様に定義されています．
```python
async def request(self, request_info: RequestInformation) -> RequestResponse
```
- **request_info `RequestInformation`**
  手順3で作成したリクエスト情報オブジェクトをそのまま渡します．

この関数を実行すると，リクエストを送信し，リクエスト先サーバーからレスポンスが来るまで待機します．  
`RequestResponse`インスタンスへレスポンスデータが格納され渡されます．  
これには以下の変数が定義されています．
- **status_code `Integer`**
  レスポンスのステータスコードが入ります．
- **reason `String`**
  レスポンスのステータスコードの理由が入ります．
- **ok `Boolean`**
  リクエストの成功フラグが入ります．
- **headers `CIMultiDictProxy[str]`**
  レスポンスヘッダが入ります．
- **json `Any`**
  レスポンスのJsonペイロードが入ります．
- **text `String`**
  レスポンスの文字列データが入ります．

*`json`と`text`は，同じデータをそれぞれのデータ型にデコードしたものが入ります．`text`はデコードに失敗した場合は`""`が入ります．