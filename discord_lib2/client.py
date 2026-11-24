import asyncio
import platform
import time

from discord_lib2.logger import Logger
from discord_lib2.runtime.core import Runtime
from discord_lib2.event import GatewayEvent
from discord_lib2.command.terminal_command import TerminalCommand
from discord_lib2.command.application_command import GlobalApplicationCommand, GuildApplicationCommand

class ApplicationCommandRegistError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class ApplicationCommandExistsException(ApplicationCommandRegistError):
  def __init__(self, name: str, guild_id: str|None=None) -> None:
    super().__init__(f"command \"{name}\" is dumplicated in {"global command" if guild_id is None else f"guild command: {guild_id}"}")

class ApplicationCommandRegister:
  def __init__(self) -> None:
    # {"guild_id": {"appcom_name": <appcom_object>}}
    self.ac_guilds: dict[str, dict[str, GuildApplicationCommand]] = {}
    # {"appcom_name": <appcom_object>}
    self.ac_globals: dict[str, GlobalApplicationCommand] = {}

  def __type_check(self, command_obj: GuildApplicationCommand|GlobalApplicationCommand, target_guild: str|None):
    if isinstance(command_obj, GuildApplicationCommand):
      if target_guild is None:
        raise ApplicationCommandRegistError(f"Need argument \"target_guild\"")
      if target_guild != "any":
        try:
          int(target_guild)
        except ValueError:
          raise ApplicationCommandRegistError(f"\"target_guild\" need \"any\" or guild_id (snowflake id)")

  def __dumplicate_check(self, name, target_guild: str|None):
    if target_guild is None:
      if name in self.ac_globals:
        raise ApplicationCommandExistsException(name)
    else:
      if target_guild == "any":
        for guild, value in self.ac_guilds.items():
          if name in value:
            raise ApplicationCommandExistsException(name, guild)
      else:
        if name in self.ac_guilds[target_guild]:
          raise ApplicationCommandExistsException(name, target_guild)

  def __regist(self, command_obj: GuildApplicationCommand|GlobalApplicationCommand, target_guild: str):
    if isinstance(command_obj, GuildApplicationCommand):
      if target_guild not in self.ac_guilds:
        self.ac_guilds[target_guild] = {}
      self.ac_guilds[target_guild][command_obj.name] = command_obj
    else:
      self.ac_globals[command_obj.name] = command_obj

  def add_command(self, command_obj: GuildApplicationCommand|GlobalApplicationCommand, target_guild: str):
    self.__type_check(command_obj, target_guild)
    self.__dumplicate_check(command_obj.name, target_guild)
    self.__regist(command_obj, target_guild)

  def get_appcoms(self):
    return {"guilds": self.ac_guilds, "globals": self.ac_globals}


class Bot:
  __INTENT_V_GUILDS                         = 1 << 0
  __INTENT_V_GUILD_MEMBERS                  = 1 << 1
  __INTENT_V_GUILD_MODERATION               = 1 << 2
  __INTENT_V_GUILD_EXPRESSIONS              = 1 << 3
  __INTENT_V_GUILD_INTEGRATIONS             = 1 << 4
  __INTENT_V_GUILD_WEBHOOKS                 = 1 << 5
  __INTENT_V_GUILD_INVITES                  = 1 << 6
  __INTENT_V_GUILD_VOICE_STATES             = 1 << 7
  __INTENT_V_GUILD_PRESENCES                = 1 << 8
  __INTENT_V_GUILD_MESSAGES                 = 1 << 9
  __INTENT_V_GUILD_MESSAGE_REACTIONS        = 1 << 10
  __INTENT_V_GUILD_MESSAGE_TYPING           = 1 << 11
  __INTENT_V_DIRECT_MESSAGES                = 1 << 12
  __INTENT_V_DIRECT_MESSAGE_REACTIONS       = 1 << 13
  __INTENT_V_DIRECT_MESSAGE_TYPING          = 1 << 14
  __INTENT_V_MESSAGE_CONTENT                = 1 << 15
  __INTENT_V_GUILD_SCHEDULED_EVENT          = 1 << 16
  __INTENT_V_AUTO_MODERATION_CONFIGURATION  = 1 << 20
  __INTENT_V_AUTO_MODERATION_EXECUTION      = 1 << 21
  __INTENT_V_GUILD_MESSAGE_POLLS            = 1 << 24
  __INTENT_V_DIRECT_MESSAGE_POLLS           = 1 << 25

  def __init__(self, bot_token: str):
    self.bot_token        = bot_token
    self.os_type          = platform.system()
    self.__application_command_register = ApplicationCommandRegister()

    self.enable_guilds                         = True
    self.enable_guild_members                  = False
    self.enable_guild_moderation               = False
    self.enable_guild_expressions              = False
    self.enable_guild_integrations             = False
    self.enable_guild_webhooks                 = False
    self.enable_guild_invites                  = False
    self.enable_guild_voice_states             = False
    self.enable_guild_presences                = False
    self.enable_guild_messages                 = False
    self.enable_guild_message_reactions        = False
    self.enable_guild_message_typing           = False
    self.enable_direct_messages                = False
    self.enable_direct_message_reactions       = False
    self.enable_direct_message_typing          = False
    self.enable_message_content                = False
    self.enable_guild_scheduled_event          = False
    self.enable_auto_moderation_configuration  = False
    self.enable_auto_moderation_execution      = False
    self.enable_guild_message_polls            = False
    self.enable_direct_message_polls           = False
  
  def __calc_bot_intent(self) -> None:
    self.bot_intent = 0
    if self.enable_guilds:                        self.bot_intent += self.__INTENT_V_GUILDS
    if self.enable_guild_members:                 self.bot_intent += self.__INTENT_V_GUILD_MEMBERS
    if self.enable_guild_moderation:              self.bot_intent += self.__INTENT_V_GUILD_MODERATION
    if self.enable_guild_expressions:             self.bot_intent += self.__INTENT_V_GUILD_EXPRESSIONS
    if self.enable_guild_integrations:            self.bot_intent += self.__INTENT_V_GUILD_INTEGRATIONS
    if self.enable_guild_webhooks:                self.bot_intent += self.__INTENT_V_GUILD_WEBHOOKS
    if self.enable_guild_invites:                 self.bot_intent += self.__INTENT_V_GUILD_INVITES
    if self.enable_guild_voice_states:            self.bot_intent += self.__INTENT_V_GUILD_VOICE_STATES
    if self.enable_guild_presences:               self.bot_intent += self.__INTENT_V_GUILD_PRESENCES
    if self.enable_guild_messages:                self.bot_intent += self.__INTENT_V_GUILD_MESSAGES
    if self.enable_guild_message_reactions:       self.bot_intent += self.__INTENT_V_GUILD_MESSAGE_REACTIONS
    if self.enable_guild_message_typing:          self.bot_intent += self.__INTENT_V_GUILD_MESSAGE_TYPING
    if self.enable_direct_messages:               self.bot_intent += self.__INTENT_V_DIRECT_MESSAGES
    if self.enable_direct_message_reactions:      self.bot_intent += self.__INTENT_V_DIRECT_MESSAGE_REACTIONS
    if self.enable_direct_message_typing:         self.bot_intent += self.__INTENT_V_DIRECT_MESSAGE_TYPING
    if self.enable_message_content:               self.bot_intent += self.__INTENT_V_MESSAGE_CONTENT
    if self.enable_guild_scheduled_event:         self.bot_intent += self.__INTENT_V_GUILD_SCHEDULED_EVENT
    if self.enable_auto_moderation_configuration: self.bot_intent += self.__INTENT_V_AUTO_MODERATION_CONFIGURATION
    if self.enable_auto_moderation_execution:     self.bot_intent += self.__INTENT_V_AUTO_MODERATION_EXECUTION
    if self.enable_guild_message_polls:           self.bot_intent += self.__INTENT_V_GUILD_MESSAGE_POLLS
    if self.enable_direct_message_polls:          self.bot_intent += self.__INTENT_V_DIRECT_MESSAGE_POLLS

  def add_application_command(self, command_object: GlobalApplicationCommand | GuildApplicationCommand, target_guild: str=""):
    self.__application_command_register.add_command(command_object, target_guild)

  def boot(self, event: GatewayEvent, logger: Logger, terminal_command: TerminalCommand | None=None, bootcycle: int=-1, proxy: str | None=None):
    self.__calc_bot_intent()
    if terminal_command is None:
      terminal_command = TerminalCommand()
    __runtime = Runtime(self.bot_token, self.bot_intent, self.os_type, logger, bootcycle, event, terminal_command, self.__application_command_register.get_appcoms(), proxy)
    asyncio.run(__runtime.boot())