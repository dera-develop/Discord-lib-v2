from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache

class CacheStageInstance(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.event_functions = {
      "STAGE_INSTANCE_CREATE": self.stage_instance_create,
      "STAGE_INSTANCE_UPDATE": self.stage_instance_update,
      "STAGE_INSTANCE_DELETE": self.stage_instance_delete
    }

  def __update_stage_instance(self, stage_instance_data: dict[str, Any], overwrite: bool=False):
    guild_id: str = stage_instance_data["guild_id"]
    instance_id: str = stage_instance_data["id"]
    super()._update_cache_dict(stage_instance_data, self.data_cache.data.guilds[guild_id].stage_instances, DataGuildCache.StageInstance, instance_id, overwrite=overwrite)

  async def stage_instance_create(self, event_data: dict[str, Any]):
    self.__update_stage_instance(event_data, True)

  async def stage_instance_update(self, event_data: dict[str, Any]):
    self.__update_stage_instance(event_data)

  async def stage_instance_delete(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    instance_id: str = event_data["id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].stage_instances, instance_id)