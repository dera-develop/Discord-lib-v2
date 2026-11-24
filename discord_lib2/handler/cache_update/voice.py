from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2

from discord_lib2.cache.user import guild as DataGuildCache

class CacheVoice(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.event_functions = {
      "VOICE_CHANNEL_EFFECT_SEND": self.voice_channel_effect_send,
      "VOICE_STATE_UPDATE": self.voice_state_update,
      "VOICE_SERVER_UPDATE": self.voice_server_update
    }

  def __update_join_count(self, guild_id: str, before_ch: str|None, current_ch: str|None):
    if before_ch != current_ch:
      if before_ch is not None:
        if before_ch in self.data_cache.data.guilds[guild_id].channels:
          self.data_cache.data.guilds[guild_id].channels[before_ch].join_member_count -= 1
      if current_ch is not None:
        if current_ch in self.data_cache.data.guilds[guild_id].channels:
          self.data_cache.data.guilds[guild_id].channels[current_ch].join_member_count += 1

  async def voice_channel_effect_send(self, event_data: dict[str, Any]):
    pass

  async def voice_state_update(self, event_data: dict[str, Any]):
    user_id: str = event_data["user_id"]
    index_guild_id = self.system_cache.channel_index.get(event_data["channel_id"])
    event_guild_id = event_data.get("guild_id")
    if index_guild_id is not None:
      guild_id = index_guild_id
    elif event_guild_id is not None:
      guild_id = event_guild_id
    else:
      return
    try:
      before_vcch_id = self.data_cache.data.guilds[guild_id].members[user_id].voice_state.channel_id
    except KeyError:
      before_vcch_id = None
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, user_id, "voice_state")
    current_vcch_id = self.data_cache.data.guilds[guild_id].members[user_id].voice_state.channel_id
    self.__update_join_count(guild_id, before_vcch_id, current_vcch_id)

  async def voice_server_update(self, event_data: dict[str, Any]):
    pass