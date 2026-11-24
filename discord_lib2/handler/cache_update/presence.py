from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache
from discord_lib2.cache.user import user as DataUserCache

class CachePresence(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "PRESENCE_UPDATE": self.presence_update,
      "TYPING_START": self.typing_start,
      "USER_UPDATE": self.user_update
    }

  async def presence_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user"]["id"]
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, user_id, "presence")

  async def typing_start(self, event_data: dict[str, Any]):
    pass

  async def user_update(self, event_data: dict[str, Any]):
    user_id: str = event_data["id"]
    super()._update_cache_dict(event_data, self.data_cache.data.users, DataUserCache.User, user_id)