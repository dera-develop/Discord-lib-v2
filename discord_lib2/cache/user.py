from dataclasses import dataclass

from discord_lib2.objects.http_request.base import b_user
from discord_lib2.objects.http_request.base import b_guild
from discord_lib2.objects.http_request.base import b_channel

snowflake = str
ISO8601timestamp = str

#########################################################################################
# User Objects
#########################################################################################
class User:
  user: b_user.User | None = None
  joined_guilds: list[snowflake] | None = None

#########################################################################################
# Channel Objects
#########################################################################################
class Guild:
  channels: dict[snowflake, b_channel.Channel]
  members: dict[snowflake, b_guild.GuildMember]

#########################################################################################

class Data:
  users: dict[snowflake, User] = {}
  guilds: dict[snowflake, Guild] = {}

class DataCacheVault:
  data: Data = Data()
  additional = {}