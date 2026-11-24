from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

class CacheMessage(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "MESSAGE_CREATE": self.message_create,
      "MESSAGE_UPDATE": self.message_update,
      "MESSAGE_DELETE": self.message_delete,
      "MESSAGE_DELETE_BULK": self.message_delete_bulk,
      "MESSAGE_REACTION_ADD": self.message_reaction_add,
      "MESSAGE_REACTION_REMOVE": self.message_reaction_remove,
      "MESSAGE_REACTION_REMOVE_ALL": self.message_reaction_remove_all,
      "MESSAGE_REACTION_REMOVE_EMOJI": self.message_reaction_remove_emoji
    }

  async def message_create(self, event_data: dict[str, Any]):
    pass

  async def message_update(self, event_data: dict[str, Any]):
    pass

  async def message_delete(self, event_data: dict[str, Any]):
    pass

  async def message_delete_bulk(self, event_data: dict[str, Any]):
    pass

  async def message_reaction_add(self, event_data: dict[str, Any]):
    pass

  async def message_reaction_remove(self, event_data: dict[str, Any]):
    pass

  async def message_reaction_remove_all(self, event_data: dict[str, Any]):
    pass

  async def message_reaction_remove_emoji(self, event_data: dict[str, Any]):
    pass
