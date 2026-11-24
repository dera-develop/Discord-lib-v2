from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache

class CacheInvite(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.event_functions = {
      "INVITE_CREATE": self.invite_create,
      "INVITE_DELETE": self.invite_delete
    }

  async def invite_create(self, event_data: dict[str, Any]):
    unique_code: str = event_data["code"]
    guild_id: str|None = self.system_cache.channel_index.get(event_data["channel_id"])
    if guild_id is None:  return
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].invites, DataGuildCache.Invite, unique_code, overwrite=True)

  async def invite_delete(self, event_data: dict[str, Any]):
    unique_code: str = event_data["code"]
    guild_id: str|None = self.system_cache.channel_index.get(event_data["channel_id"])
    if guild_id is None:  return
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].invites, unique_code)
    self.system_cache.channel_index.delete(event_data["channel_id"])