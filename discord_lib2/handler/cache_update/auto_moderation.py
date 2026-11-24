from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

class CacheAutoModeration(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "AUTO_MODERATION_RULE_CREATE": self.rule_create,
      "AUTO_MODERATION_RULE_UPDATE": self.rule_update,
      "AUTO_MODERATION_RULE_DELETE": self.rule_delete,
      "AUTO_MODERATION_ACTION_EXECUTION": self.action_execution,
    }

  async def rule_create(self, event_data: dict[str, Any]):
    pass

  async def rule_update(self, event_data: dict[str, Any]):
    pass

  async def rule_delete(self, event_data: dict[str, Any]):
    pass

  async def action_execution(self, event_data: dict[str, Any]):
    pass