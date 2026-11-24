from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

class CachePoll(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "MESSAGE_POLL_VOTE_ADD": self.message_poll_vote_add,
      "MESSAGE_POLL_VOTE_REMOVE": self.message_poll_vote_remove
    }

  async def message_poll_vote_add(self, event_data: dict[str, Any]):
    pass

  async def message_poll_vote_remove(self, event_data: dict[str, Any]):
    pass