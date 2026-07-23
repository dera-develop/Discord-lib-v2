from dataclasses import dataclass

from discord_lib2.objects.http_request.base import b_user
from discord_lib2.objects.http_request.base import b_guild

snowflake = str

class Exclude:
  pass

@dataclass
class Ready:
  @dataclass
  class Application:
    id: snowflake
    flags: int
    flags_new: str

  v: int
  user: b_user.User
  guilds: list[b_guild.UnavailableGuild]
  session_id: str
  resume_gateway_url: str
  application: Application
  shard: list[list[int]] | Exclude = Exclude()