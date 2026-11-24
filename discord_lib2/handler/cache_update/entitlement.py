from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

class CacheEntitlement(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "ENTITLEMENT_CREATE": self.entitlement_create,
      "ENTITLEMENT_UPDATE": self.entitlement_update,
      "ENTITLEMENT_DELETE": self.entitlement_delete
    }

  async def entitlement_create(self, event_data: dict[str, Any]):
    pass

  async def entitlement_update(self, event_data: dict[str, Any]):
    pass

  async def entitlement_delete(self, event_Data: dict[str, Any]):
    pass