# Terminal Command
このライブラリでは，ターミナルでコマンドを実行することができます．
いくつかの標準コマンドと，ユーザーが任意で登録可能なコマンドがあります．

## 機能
ターミナルへコマンドを入力することで，関数を実行することができます．
入力形式は，
```shell
command_name arg1 arg2...
```
となります．

## 標準コマンド
ライブラリには，デフォルトでコマンドが用意されています．
|コマンド名|引数|機能|
|--|--|--|
|stop|N/A|Gateway接続を終了し，プログラムを終了します．|
|reconnect|N/A|Gateway接続を終了し，再接続を行います．|

## ユーザー定義コマンド
ユーザーが任意でターミナルコマンドを登録することができます．
##### 注意
**アプリを実行しているターミナルで実行できるコマンドです．**
**DiscordBotがイベント経由で受信するコマンドとは異なります．**

### 設定方法
必要なクラスは，`discord_lib2/command.py`内にある`TerminalCommand`クラスです．
型ヒントが使えるようになるので，`discord_lib2/objects/resources.py`内にある`UserTerminalCommandResources`クラスを併せてimportしておくことをお勧めします．
```python
from discord_lib2.command import TerminalCommand
from discord_lib2.objects.resources import UserTerminalCommandResources
```

コマンドを定義する手順は，以下の通りです．

#### 1. 関数定義
コマンド内容の関数を定義します．定義する際，以下2つの条件を満たす必要があります．
- 関数は，`async def`を使用する必要があります．
- 引数として，`args` `resources`を定義する必要があります．
  - `args`
  `list[str]`型です．コマンド実行時の入力内容が渡されます．
  `command arg1 arg2...`と渡されると，`args`は`["command", "arg1", "arg2"...]`となります．
  - `resources`
  `UserTerminalCommandResources`型です．Overviewの[キャッシュ項目](overview.md#キャッシュ)に記述されている構造と同一の構造になっています．
  唯一，`logger`の名前のみ，`TUC(Terminal User Command)`となっています．
HttpAPIリクエストボディーの作成，Gatewayリクエストの送信等は，Gatewayイベントのユーザー定義関数と同様に行うことができます．

#### 2. 関数の登録
作成したターミナルコマンド関数を登録します．
`TerminalCommand`インスタンスを作成し，`add_command`メゾッドを通してコマンドを登録します．
`command_name`に設定した文字列をターミナルへ入力すると，`function`に設定した関数が呼び出されます．
```python
terminal_command = TerminalCommand()

terminal_command.add_command("command1_name", command1_function)
terminal_command.add_command("command2_name", command2_function)
```
##### 注意
`command_name`に登録する際，標準コマンドと重複した名前でコマンド名の登録を行うことは出来ますが，実行時には標準コマンドが実行されます．
実装されている標準コマンドは，[標準コマンドセクション](#標準コマンド)を参照してください．

#### 3. Botインスタンスへ渡す
`bot.boot()`関数実行時に，引数として渡します．
必須ではないため，デフォルト値は`None`に設定されています．
```python
bot.boot(..., terminal_command=terminal_command)
```

### サンプルプログラム
```python
from discord_lib2.command import TerminalCommand
from discord_lib2.objects.resources import UserTerminalCommandResources

async def show_joined_guild_ids(args: list[str], resources: UserTerminalCommandResources):
  ids = list(resources.cache.data.guilds.keys())
  resources.logger.info(f"joinied guild ids: {ids}")

terminal_command = TerminalCommand()
terminal_command.add_command("sgi", show_joined_guild_ids)

bot.boot(..., terminal_command=terminal_command)
```
