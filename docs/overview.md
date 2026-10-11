### Documents
- [OVERVIEW](#overview)
- [Gateway Event](gateway_event.md)
- [APPLICATION COMMAND](applicarion_commands.md)
- [TERMINAL COMMAND](user_terminal_commands.md)

# OVERVIEW  
## 前提  
このライブラリは，GATEWAYイベントを使用したボットの作成を前提としたライブラリです．  
HTTPSリクエストのみを行うボットの作成には対応していません．  
  
## サンプルコード  
サンプルコード群は，[ここ](../sample/)に保存されています．  
ここでは，この中にある [hello_world.py](../sample/hello_world.py)をベースに解説を行います．  
```python  
# sample/hello_world.py  
  
from discord_lib2.client import Bot  
from discord_lib2.logger import Logger  
from discord_lib2.event import GatewayEvent  
  
bot = Bot("your_bot_token")  
  
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
bot = Bot("your_bot_token")  
```  
  
#### 引数  
- `bot_token` `str`  
ボットのトークンを設定します．  
このトークンは，Gateway接続の認証や，APIへのリクエストの認証に使用されます．  
  
#### インテントの設定  
Gatewayイベントを受信するための各種権限であるインテントの設定をこのBotクラスで行います．  
Botクラスのインスタンスを使い，起動前に設定を行います．  
インテントの項目は`bool`型で定義されており，値を`True`に変更することで自動的に値が計算され，`Identify`イベント時に送信されます．  
```python  
bot = Bot("your_bot_token")  
  
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
bot.boot(event, logger, terminal_command, bootcycle, proxy)  
```  
##### 各引数
- `event`(`GatewayEvent`)
ゲートウェイイベントを受信した際の実行関数を定義したクラスインスタンスを渡します．  
このクラスの詳細は，後述の[GatewayEventクラス](#GatewayEvent(ユーザーイベント)クラス)を参照してください．
- `logger`(`Logger`)
ロガーのクラスインスタンスを渡します．  
このクラスの詳細は，後述の[Loggerクラス](#Loggerクラス)を参照してください．
- `terminal_command`(`TerminalCommand`)(任意)
プログラムを実行しているターミナルで実行可能なコマンドのクラスインスタンスを渡します．  
この引数の指定は任意です．指定しない場合，デフォルトターミナルコマンドのみが使用できます．  
このクラスの詳細は，[Application Commandドキュメント](applicarion_commands.md)を参照してください．
- bootcycle(`int`)(任意)
`Gateway`接続の再接続回数を指定します．初回接続の回数も含まれています．  
この引数の指定は任意です．デフォルトで`-1`が設定されており，この状態では再接続回数が無制限となります．
- `proxy`(`str`)(任意)
`httpAPI`のリクエスト，`Gateway`接続で使用するプロキシサーバーを指定します．  
指定する際は，サーバーのURLとポート番号を両方含める必要があります．
```
bot.boot(..., proxy="your.proxy.server.URL:port")
```
  
### Loggerクラス  
ターミナルやファイルへのログ出力を管理するクラスです．`Logging`ライブラリをベースに作成しています．  
`Logging`ライブラリに対応する形であれば，ユーザーが自由にログの出力先や出力レベルを設定できます．  
  
#### ユーザー設定  
ユーザー自身で設定を行う際は，`Logger`クラス内の`logger`変数が，Loggingの親に設定されているので，そこへハンドラを追加してください．最小レベルは`Debug`になっています．  
```python  
logger = Logger()  
logger.logger # loggingの親変数 ここに設定していく  
```  
  
##### ⚠注意⚠  
Discord_Lib2.0では，`asyncio`を使用した非同期処理を使用し構築されています．  
そのため，ユーザー自身で設定を行う際は，それに対応させた形でのログ出力を行う必要があります．  
  
#### デフォルト設定  
もし設定が面倒である場合は，ログ出力の設定関数を用意してあるので，それを利用することができます．  
```python  
logger = Logger()  
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
詳細は，[Gateway Eventドキュメント](./gateway_event.md)を参照してください．