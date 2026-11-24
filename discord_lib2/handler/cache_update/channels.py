from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache

class CacheChannels(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.event_functions = {
      "CHANNEL_CREATE": self.channel_create,
      "CHANNEL_UPDATE": self.channel_update,
      "CHANNEL_DELETE": self.channel_delete,
      "CHANNEL_INFO": self.channel_info,
      "VOICE_CHANNEL_STATUS_UPDATE": self.voice_channel_status_update,
      "VOICE_CHANNEL_START_TIME_UPDATE": self.voice_channel_start_time_update,
      "THREAD_CREATE": self.thread_create,
      "THREAD_UPDATE": self.thread_update,
      "THREAD_DELETE": self.thread_delete,
      "THREAD_LIST_SYNC": self.thread_list_sync,
      "THREAD_MEMBER_UPDATE": self.thread_member_update,
      "THREAD_MEMBERS_UPDATE": self.thread_members_update,
      "CHANNEL_PINS_UPDATE": self.channel_pins_update
    }

  def __add_index(self, channel_id: str, guild_id: str):
    self.system_cache.channel_index.add(channel_id, guild_id)

  def __delete_index(self, channel_id: str):
    self.system_cache.channel_index.delete(channel_id)

  def __update_channel(self, channel_data: dict[str, Any], overwrite: bool=False):
    channel_id: str = channel_data["id"]
    guild_id: str = channel_data["guild_id"]
    super()._update_cache_dict(channel_data, self.data_cache.data.guilds[guild_id].channels, DataGuildCache.Channel, channel_id, overwrite=overwrite)
    self.__add_index(channel_id, guild_id)

  def __update_thread(self, thread_data: dict[str, Any], overwrite: bool=False):
    thread_id: str = thread_data["id"]
    guild_id: str = thread_data["guild_id"]
    parent_id: str|None = thread_data.get("parent_id")
    super()._update_cache_dict(thread_data, self.data_cache.data.guilds[guild_id].threads, DataGuildCache.Thread, thread_id, overwrite=overwrite)
    self.__add_index(thread_id, guild_id)
    if parent_id is None: return
    super()._add_cache_list(self.data_cache.data.guilds[guild_id].channels[parent_id].threads, thread_id)

  def __update_thread_member(self, guild_id: str, member: dict[str, Any], overwrite: bool=False):
      thread_id: str = member["id"]
      user_id: str = member["user_id"]
      super()._update_cache_dict(member, self.data_cache.data.guilds[guild_id].threads[thread_id].members, DataGuildCache.ThreadMember, user_id, overwrite=overwrite)

  async def channel_create(self, event_data: dict[str, Any]):
    self.__update_channel(event_data, True)

  async def channel_update(self, event_data: dict[str, Any]):
    self.__update_channel(event_data)

  async def channel_delete(self, event_data: dict[str, Any]):
    channel_id: str = event_data["id"]
    guild_id: str = event_data["guild_id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].channels, channel_id)
    self.__delete_index(channel_id)

  async def channel_info(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    channels: list[dict[str, Any]] = event_data["channels"]
    super()._update_sync(channels, self.data_cache.data.guilds[guild_id].channels, DataGuildCache.Channel, "id")

  async def voice_channel_status_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    channel_id: str = event_data["id"]
    self.data_cache.data.guilds[guild_id].channels[channel_id].status = event_data["status"]

  async def voice_channel_start_time_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    channel_id: str = event_data["id"]
    self.data_cache.data.guilds[guild_id].channels[channel_id].voice_start_time = event_data.get("voice_start_time")

  async def thread_create(self, event_data: dict[str, Any]):
    self.__update_thread(event_data, True)

  async def thread_update(self, event_data: dict[str, Any]):
    self.__update_thread(event_data)

  async def thread_delete(self, event_data: dict[str, Any]):
    thread_id: str = event_data["id"]
    guild_id: str = event_data["guild_id"]
    parent_id: str|None = event_data.get("parent_id")
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].threads, thread_id)
    self.__delete_index(thread_id)
    if parent_id is None: return
    super()._delete_cache_list(self.data_cache.data.guilds[guild_id].channels[parent_id].threads, thread_id)

  async def thread_list_sync(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    threads: list[dict[str, Any]] = event_data["threads"]
    members: list[dict[str, Any]] = event_data["members"]
    super()._update_sync(threads, self.data_cache.data.guilds[guild_id].threads, DataGuildCache.Thread, "id", overwrite=True)
    for member in members:
      self.__update_thread_member(guild_id, member, True)

  async def thread_member_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    thread_id = event_data["id"]
    self.data_cache.data.guilds[guild_id].threads[thread_id].member.update(event_data)

  async def thread_members_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    thread_id: str = event_data["id"]
    member_count: int = event_data["member_count"]
    members: list[dict[str, Any]] = event_data.get("added_members", [])
    removed_members: list[str] = event_data.get("removed_member_ids", [])
    self.data_cache.data.guilds[guild_id].threads[thread_id].member_count = member_count
    for member_id in removed_members:
      super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].threads[thread_id].members, member_id)
    for member in members:
      self.__update_thread_member(guild_id, member)

  async def channel_pins_update(self, event_data: dict[str, Any]):
    self.data_cache.data.guilds["aaaa"].channels["aaa"].last_pin_timestamp
    guild_id: str|None = event_data.get("guild_id")
    channel_id: str = event_data["channel_id"]
    if guild_id is None: return
    self.data_cache.data.guilds[guild_id].channels[channel_id].last_pin_timestamp = event_data.get("last_pin_timestamp")