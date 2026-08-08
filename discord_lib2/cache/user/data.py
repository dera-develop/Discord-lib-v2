from discord_lib2.cache.user import guild
from discord_lib2.cache.user import user

snowflake = str
ISO8601timestamp = str
#########################################################################################

class Data:
  users: dict[snowflake, user.User] = {}
  guilds: dict[snowflake, guild.GuildCache] = {}

class DataCacheVault:
  data: Data = Data()
  additional = {}

#########################################################################################