from discord_lib2.cache.user import guild
from discord_lib2.cache.user import user

snowflake = str
ISO8601timestamp = str
#########################################################################################

class Data:
  def __init__(self) -> None:
    self.users: dict[snowflake, user.User] = {}
    self.guilds: dict[snowflake, guild.GuildCache] = {}

class DataCacheVault:
  def __init__(self) -> None:
    self.data: Data = Data()
    self.additional = {}

#########################################################################################