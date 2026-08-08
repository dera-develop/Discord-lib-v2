import os
import asyncio

from discord_lib2.logger import Logger
from discord_lib2.runtime import Runtime
from discord_lib2.event import GatewayEvent

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

  enable_guilds                         = True
  enable_guild_members                  = False
  enable_guild_moderation               = False
  enable_guild_expressions              = False
  enable_guild_integrations             = False
  enable_guild_webhooks                 = False
  enable_guild_invites                  = False
  enable_guild_voice_states             = False
  enable_guild_presences                = False
  enable_guild_messages                 = False
  enable_guild_message_reactions        = False
  enable_guild_message_typing           = False
  enable_direct_messages                = False
  enable_direct_message_reactions       = False
  enable_direct_message_typing          = False
  enable_message_content                = False
  enable_guild_scheduled_event          = False
  enable_auto_moderation_configuration  = False
  enable_auto_moderation_execution      = False
  enable_guild_message_polls            = False
  enable_direct_message_polls           = False


  bot_intent = 0

  def __init__(self, bot_token: str, os_type: str):
    self.bot_token        = bot_token
    self.os_type          = os_type
    self.PATH_MAINSCRIPT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
  def __calc_bot_intent(self) -> None:
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

  def boot(self, event: GatewayEvent, logger: Logger, bootcycle: int=-1):
    self.__calc_bot_intent()
    __runtime = Runtime(self.bot_token, self.bot_intent, self.os_type, logger, bootcycle, event)
    asyncio.run(__runtime.boot())