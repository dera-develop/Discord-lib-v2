# Application Command   
アプリケーションコマンドの定義をすることができます．   
アプリケーションコマンドの詳細については，[Discord公式ドキュメント[ApplicationCommands]](https://docs.discord.com/developers/interactions/application-commands)を参照してください．   
  
## サンプルコード   
ギルドアプリケーションコマンドを定義するサンプルコードです．   
このコードでは，`/examplecommand`という名前のコマンドを作成します．   
オプションとして，`string(文字列引数)`,`number(数値引数)`を指定できます．   
```python   
# guild application command example

from discord_lib2.client import Bot
from discord_lib2.logger import Logger
from discord_lib2.event import GatewayEvent
from discord_lib2.command import application_command
from discord_lib2.objects.resources import ApplicationCommandResources

from discord_lib2.objects.http_request.body import b_interaction

bot = Bot("bot_token", "os_type")

logger = Logger()
logger.create_default_handler("log_dir_path")

class UserEvent(GatewayEvent):
  ...
event = UserEvent()

class ExampleCommand(application_command.GuildApplicationCommand):
  name = "ping"
  description = "ping"
  async def command_function(self, interaction: application_command.ApplicationCommandInteraction, resources: ApplicationCommandResources, args: application_command.AppComArgs):
    req_data = resources.http_api.load_request(b_interaction.CreateInteractionResponse(
      type=4,
      data=b_interaction.InteractionCallbackData(
        content="pong",
        flags=64
      )))
    await resources.http_api.request(req_data)

bot.add_application_command(ExampleCommand(), "guild_id")

bot.boot(event, logger) 
```   
  
## 使用するクラス   
`discord_lib2/command/application_command`内にあるクラスを使用します．   
使用する際は各クラスを**オーバーライド**して使用します．   
オーバーライドしたクラスを定義する際，それぞれ値を設定する必要があります．   
各要素の値の変数型は，公式ドキュメントまたは型ヒントを参照してください．   
### 共通変数   
各クラスでは，`name`と`description`を定義する必要があります．   
各要素は共に`String`型です．   
また，任意で`name_localizations`と`description_localizations`を定義します．   
これらは関数を使って定義するか，直接辞書型での定義を行います．   
#### 関数による定義   
```python   
add_name_localization(locale: str, name: str)   
add_description_localization(locale: str, description: str)   
```   
これらの関数は，`__init__()`内で行う必要があります．   
定義の際，`super().__init__()`を削除しないでください．   
```python   
class Command(...):
  ...
  def __init__(self) -> None:
    super().__init__() # do not delete
    self.add_name_localization("locale_1", "locale_1_name")
    self.add_name_localization("locale_2", "locale_2_name")
    self.add_description_localization("locale_1", "locale_1_description")
    self.add_description_localization("locale_2", "locale_2_description")
```   
関数を使用し定義を行うと，localeと重複の検証が行われます．   
設定不可能なlocaleを定義，または既に定義されているlocaleを定義しようとした際に例外が発生します．   
  
#### 辞書型による直接定義   
直接指定する場合は，他要素と同じく変数を直接定義してください．   
```python   
name_localizations = {
  "locale_1": "locale_1_name",
  "locale_2": "locale_2_name"
}
description_localizations = {
  "locale_1": "locale_1_description",
  "locale_2": "locale_2_description"
}
```   
こちらは検証が一切行われないので，形式に注意して定義してください．   
  
### 個別定義変数   
以下は，それぞれのクラスで定義を行う要素です．   
デフォルト値が設定されている場合は，   
`変数名` - `default: x`   
のように示します．   
必須の場合は，値名に`@`を付与しています．   
#### ベースクラス   
  アプリケーションコマンドを定義する際ベースとなるクラスです．   
  - `GuildApplicationCommand`クラス   
    ギルドコマンドを定義するのに使用します．   
    設定する値は，[Discord公式ドキュメント/Create Guild Application Commandリクエストセクション](https://docs.discord.com/developers/interactions/application-commands#create-guild-application-command)の`JSON Params`で示されている要素に対応します．   
    - `type` - `default: 1`   
    - `nsfw` - `default: False`   
    - `default_member_permissions`   
    - `default_permission`   
  - `GlobalApplicationCommand`クラス   
    グローバルコマンドを定義するのに使用します．   
    設定する値は，[Discord公式ドキュメント/Create Global Application Commandリクエストセクション](https://docs.discord.com/developers/interactions/application-commands#create-global-application-command)の`JSON Params`で示されている要素に対応します．   
    - `type` - `default: 1`   
    - `nsfw` - `default: False`   
    - `default_member_permissions`   
    - `default_permission`   
    - `integration_types`   
    - `contexts`   
    - `handler`   
#### サブコマンドクラス   
  それぞれのクラスで設定する値は，[Discord公式ドキュメント/Application command](https://docs.discord.com/developers/interactions/application-commands#application-command-object-application-command-option-structure)の`Application Command Option`で示されている要素に対応します．   
  - `SubCommand`クラス   
    サブコマンドを定義するのに使用します．   
  - `SubCommandGroup`クラス   
    サブコマンドグループを定義するのに使用します．   
#### オプション   
  それぞれのクラスで設定する値は，[Discord公式ドキュメント/Application command](https://docs.discord.com/developers/interactions/application-commands#application-command-object-application-command-option-structure)の`Application Command Option`で示されている要素に対応します．   
  - `String`クラス   
    文字列オプションを定義するのに使用します．   
    - \*`choices`   
    - `min_length`   
    - `max_length`   
  - `Integer`クラス   
    整数オプションを定義するのに使用します．   
    - \*`choices`   
    - `min_value`   
    - `max_value`   
    - `autocomplete`   
  - `Boolean`クラス   
    正誤オプションを定義するのに使用します．   
  - `User`クラス   
    ユーザーオプションを定義するのに使用します．   
  - `Channel`クラス   
    チャンネルオプションを定義するのに使用します．   
    - `channel_type`   
  - `Role`クラス   
    ロールオプションを定義するのに使用します．   
  - `Mentionable`クラス   
    メンションオプションを定義するのに使用します．   
  - `Number`クラス   
    - \*`choices`   
    - `min_value`   
    - `max_value`   
    - `autocomplete`   
    数値オプションを定義するのに使用します．   
  - `Attachment`クラス   
    アタッチメントオプションを定義するのに使用します．   
    - `file_types`   
  
\* `application_command/Choice`クラスの**インスタンス**の配列を設定します．**オーバーライドクラスではありません**．   
  
### コールバック   
`Gateway`接続のイベントの一つである`InteractionCreate`イベントを受信した際，イベントを受信してから3秒以内に応答（コールバックリクエスト）を行う必要があります．　　
使用するリクエストオブジェクトは，`discord_lib2.objects.http_request.body.b_interaction`にあります．　　  
リクエストで使用する`interaction.id`,`interaction.token`は，`command_function`で渡されるオブジェクト(`interaction: application_command.ApplicationCommandInteraction`)に含まれています．
リクエストは，Overviewに記載されている方法と同様の方法で送信します．([Overview:HttpAPI](overview.md#HttpAPI))  
コールバックの詳細については，[Discord公式ドキュメント/Responding to an Interaction](https://docs.discord.com/developers/interactions/receiving-and-responding#responding-to-an-interaction)を参照してください．   
  
## 定義   
### 構造定義   
クラスの定義は，[ベースクラス](#ベースクラス)を基準として階層構造で定義することをお勧めします．   
```python   
class Command(application_command.GuildApplicationCommand):
  name = "command"
  description = "description"
  class SubCommandGroup(application_command.SubCommandGroup):
    name = "subcommandgroup"
    description = "subcommand group description"
    class SubCommand1(application_command.SubCommand):
      name = "subcommand1"
      description = "subcommand1 description"
    class SubCommand2(application_command.SubCommand):
      name = "subcommand2"
      description = "subcommand2 description"
  class String(application_command.String):
    name = "string"
    description = "description"
  ...
```   
クラスを定義後，ベースクラス，各サブコマンドグループ，各サブコマンドへ要素を設定する必要があります．   
追加関数は，各クラスに以下のように定義されています．   
```python   
# GuildApplicationCommand / GlobalApplicationCommand
add_option(option: SubCommandGroup | SubCommand | _OptionBase)

# SubCommandGroup
add_subcommand(subcommand: SubCommand)

# SubCommand
add_option(option: _OptionBase)
```   
\* `_OptionBase`クラスは，`SubCommandGroup`,`SubCommand`を除くすべてのオプションです．   
  
これらの関数は，`name_localizations`,`description_localizations`と同じように，`__init__()`関数内で呼び出します．   
```python   
class ExampleCommand(application_command.GuildApplicationCommand):
  ...
  class StringOption(application_command.String):
    ...
  class NumberOption(application_command.Number):
    ...
  def __init__(self) -> None:
    super().__init__()
    self.add_option(self.StringOption())
    self.add_option(self.NumberOption())
```   
このコードでは，`ExampleCommand`クラスに，オプションとして`StringOption`,`NumberOption`が追加されます．   
  
### 関数定義   
コマンドが実行された際に，自動的に実行される関数を定義します．   
ここで定義した関数は，インタラクションのコールバックが作成・送信されたのちに自動的に実行されます．   
コマンド定義可能なクラスは，`GuildApplicationCommand`,`GlobalApplicationCommand`,`SubCommand`です．   
```python   
command_function(interaction: application_command.ApplicationCommandInteraction, resources: ApplicationCommandResources, args: AppComArgs)
```   
- `interaction`   
  インタラクションイベントのオブジェクトインスタンスが渡されます．   
  変数はインスタンス変数として呼び出せます．   
- `resources`   
  `ApplicationCommandResources`型です．Overviewの[リソースセクション](overview.md#resources)に記述されている構造と同一の構造になっています．唯一，`logger`の名前のみ，`ACE(Application Command Event)`となっています．   
  リクエスト等はOverviewに記載されているものと同様に行うことができます．   
- `args`   
  `AppComArgs`型です．`dict`型をオーバーライドした型です．設定したオプションをメゾッドとして呼び出せます．   
  例えば，以下のようにアプリケーションコマンドを定義し   
  ```python   
  class Command(application_command.GuildApplicationCommand):
    name = "command"
    ...
    class String(application_command.String):
      name = "inputstring"
      ...
    class Integer(application_command.Integer):
      name = "inputint"
      ...
  ```   
  アプリケーションコマンドが以下のように実行された場合   
  ```shell   
  # execute
  /command inputstring:ExampleText inputint:10
  ```   
  以下の方法のどちらかで呼び出すことができます   
  ```python   
  args.inputstring      # "ExampleText"
  args.inputint         # 10
  args["inputstring"]   # "ExampleText"
  args["inputint"]      # 10
  ```   
  引数として渡されていないオプションを呼び出した際には`None`が入ります．   
  ```shell   
  # execute   
  /command inputint:15   
  ```   
  ```python   
  args.inputint       # 15
  args.inputstring    # None
  args["inputint"]    # 15
  args["inputstring"] # KeyError
  ```   
  
## コマンドの追加   
定義が完了したら，アプリケーションコマンドクラスを`Bot`インスタンスへ渡す必要があります．   
`Bot`インスタンスにある以下のメゾッドを使用します．   
```python   
add_application_command(command_object: GlobalApplicationCommand | GuildApplicationCommand, target_guild: str="")
```   
- `command_object`   
  `GlobalApplicationCommand`または`GuildApplicationCommand`のインスタンスを渡します．オーバーライドして作成したコマンドインスタンスを渡します．   
- `target_guild`   
  `str`型です．登録するコマンドがギルドコマンド(`GuildApplicationCommand`)の場合，ギルドIDを指定する必要があります．グローバルコマンドの登録では不要です．
```python   
bot = Bot("bot_token", "os_type")
...
class GuildCommand(application_command.GuildApplicationCommand):
  ...

class GlobalCommand(application_command.GlobalApplicationCommand):
  ...

bot.add_application_command(GuildCommand(), "guild_id")
bot.add_application_command(GlobalCommand())
```   
#### ギルドコマンドの実質的なグローバル化
  登録関数の引数`target_guild`へ`String`型で`any`を指定すると，`GuildCreate`イベントを受信した全てのギルドへギルドコマンドとして登録されます．