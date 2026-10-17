from discord_lib2.cache.user import guild
from discord_lib2.cache.user import user
from discord_lib2.objects.gateway.recv_event_object import Application

from typing import Any

snowflake = str
ISO8601timestamp = str
#########################################################################################

class Data:
  def __init__(self) -> None:
    self.users: dict[snowflake, user.User] = {}
    self.guilds: dict[snowflake, guild.GuildCache] = {}
    self.application: Application = Application()

class DataCacheVault:
  def __init__(self) -> None:
    self.data: Data = Data()
    self.additional: Any = {}

#########################################################################################