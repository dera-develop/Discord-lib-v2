from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache

class CacheIntegration(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "INTEGRATION_CREATE": self.integration_create,
      "INTEGRATION_UPDATE": self.integration_update,
      "INTEGRATION_DELETE": self.integration_delete
    }

  def __update_integration(self, integration_data: dict[str, Any], guild_id: str, overwrite: bool=False):
    integration_id: str = integration_data["id"]
    super()._update_cache_dict(integration_data, self.data_cache.data.guilds[guild_id].integrations, DataGuildCache.Integration, integration_id, overwrite=overwrite)

  async def integration_create(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    self.__update_integration(event_data, guild_id, True)

  async def integration_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    self.__update_integration(event_data, guild_id)

  async def integration_delete(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    integration_id: str = event_data["id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].integrations, integration_id)