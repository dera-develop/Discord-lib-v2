from discord_lib2.Network.gateway.structure_creator import Presence

from discord_lib2.cache.system.objects.resume import Resume
from discord_lib2.cache.system.objects.gateway import Gateway

class SystemCacheVault:
  bot_token: str
  bot_intents: int
  os_type: str
  shard: list[int] | None = None
  large_threshold: int | None = None
  compress: bool | None = None
  presence: Presence | None = None
  

  resume  = Resume()
  gateway = Gateway()