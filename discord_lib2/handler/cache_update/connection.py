from logging import Logger
from typing import Any

from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.cache.user.guild import GuildCache
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import HTTPcontroller, CacheUpdateBase
from discord_lib2.network.gateway.websocket import WebsocketController

from discord_lib2.objects.gateway import request_payload

class CacheConnection(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault, gateway_controller: WebsocketController) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.gateway = gateway_controller
    self.event_functions = {
      "READY"   : self.ready,
      "RESUMED" : self.resumed
    }

  def __update_system_cache(self, event_data: dict[str, Any]):
    self.system_cache.resume.reconnect_gateway_url  = event_data["resume_gateway_url"]
    self.system_cache.resume.session_id             = event_data["session_id"]
    self.system_cache.gateway.gateway_url           = event_data["resume_gateway_url"]

  async def __request_guildmembers(self, guild_id: str):
    req_data = request_payload.RequestGuildMembers(guild_id, 0, "", True)
    await self.gateway.send(req_data.get())

  async def __init_guild_cache(self, event_data: dict[str, Any]):
    for u_guild in event_data["guilds"]:
      self.data_cache.data.guilds[u_guild["id"]] = GuildCache()
      self.data_cache.data.guilds[u_guild["id"]].id = u_guild["id"]
      self.data_cache.data.guilds[u_guild["id"]].unavailable = u_guild["unavailable"]
      if u_guild["unavailable"]:
        await self.__request_guildmembers(u_guild["id"])

  async def ready(self, event_data: dict[str, Any]):
    self.__update_system_cache(event_data)
    await self.__init_guild_cache(event_data)


  async def resumed(self, event_data: dict[str, Any]):
    return