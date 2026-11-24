from logging import Logger
from typing import Any

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import CacheUpdateBase, HTTPcontroller
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.network.gateway.websocket import WebsocketController

from discord_lib2.cache.user import guild as DataGuildCache

class CacheGuild(CacheUpdateBase):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault, gateway_controller: WebsocketController) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.gateway_controller = gateway_controller
    self.event_functions = {
      "GUILD_CREATE": self.guild_create,
      "GUILD_UPDATE": self.guild_update,
      "GUILD_DELETE": self.guild_delete,
      "GUILD_AUDIT_LOG_ENTRY_CREATE": self.guild_audit_log_entry_create,
      "GUILD_BAN_ADD": self.guild_ban_add,
      "GUILD_BAN_REMOVE": self.guild_ban_remove,
      "GUILD_EMOJIS_UPDATE": self.guild_emojis_update,
      "GUILD_STICKERS_UPDATE": self.guild_stickers_update,
      "GUILD_INTEGRATIONS_UPDATE": self.guild_integrations_update,
      "GUILD_MEMBER_ADD": self.guild_member_add,
      "GUILD_MEMBER_REMOVE": self.guild_member_remove,
      "GUILD_MEMBER_UPDATE": self.guild_member_update,
      "GUILD_MEMBER_UPDATE": self.guild_member_update,
      "GUILD_MEMBERS_CHUNK": self.guild_members_chunk,
      "GUILD_ROLE_CREATE": self.guild_role_create,
      "GUILD_ROLE_UPDATE": self.guild_role_update,
      "GUILD_ROLE_DELETE": self.guild_role_delete,
      "GUILD_SCHEDULED_EVENT_CREATE":self.guild_scheduled_event_create,
      "GUILD_SCHEDULED_EVENT_UPDATE": self.guild_scheduled_event_update,
      "GUILD_SCHEDULED_EVENT_DELETE": self.guild_scheduled_event_delete,
      "GUILD_SCHEDULED_EVENT_USER_ADD": self.guild_scheduled_event_user_add,
      "GUILD_SCHEDULED_EVENT_USER_REMOVE": self.guild_scheduled_event_user_remove,
      "GUILD_SOUNDBOARD_SOUND_CREATE": self.guild_soundboard_sound_create,
      "GUILD_SOUNDBOARD_SOUND_UPDATE": self.guild_soundboard_sound_update,
      "GUILD_SOUNDBOARD_SOUND_DELETE": self.guild_soundboard_sound_delete,
      "GUILD_SOUNDBOARD_SOUNDS_UPDATE": self.guild_soundboard_sounds_update,
      "SOUNDBOARD_SOUNDS": self.soundboard_sounds
    }

  def __update_guild_cache(self, event_data: dict[str, Any], guild_id: str):
    super()._update_cache_dict(event_data, self.data_cache.data.guilds, DataGuildCache.GuildCache, guild_id)

  def __connect_channel_thread_cache(self, guild_id: str):
    """
    親チャンネルに子スレッドIDを紐づけ
    """
    threads_in_channel: dict[str, list[str]] = {} # {"channel_id": ["thread_ids"]}
    for thread_id, thread_data in self.data_cache.data.guilds[guild_id].threads.items():
      if thread_data.parent_id is None: continue
      if thread_data.parent_id not in threads_in_channel:
        threads_in_channel[thread_data.parent_id] = []
      threads_in_channel[thread_data.parent_id].append(thread_id)
    for parent_id, thread_ids in threads_in_channel.items():
      if parent_id in self.data_cache.data.guilds[guild_id].channels:
        self.data_cache.data.guilds[guild_id].channels[parent_id].threads = thread_ids

  def __update_voice_states(self, voice_states: list[dict[str, Any]], guild_id: str):
    super()._update_sync(voice_states, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, "user_id", "voice_state", True)

  def __update_presences(self, presences: list[dict[str, Any]]):
    for presence in presences:
      guild_id: str = presence["guild_id"]
      user_id: str = presence["user"]["id"]
      super()._update_cache_dict(presence, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, user_id, "presence", True)

  def __update_guild_role(self, event_data: dict[str, Any], overwrite: bool=False):
    guild_id = event_data["guild_id"]
    role = event_data["role"]
    role_id = role["id"]
    super()._update_cache_dict(role, self.data_cache.data.guilds[guild_id].roles, DataGuildCache.Role, role_id, overwrite=overwrite)

  def __update_guild_member(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user"]["id"]
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, user_id)

  def __update_guild_scheduled_event(self, event_data: dict[str, Any], overwrite: bool=False):
    guild_id: str = event_data["guild_id"]
    event_id: str = event_data["id"]
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].guild_scheduled_events, DataGuildCache.GuildScheduledEvent, event_id, overwrite=overwrite)

  def __update_guild_soundboard_sound(self, event_data: dict[str, Any], overwrite: bool=False):
    guild_id: str = event_data["guild_id"]
    sound_id: str = event_data["sound_id"]
    super()._update_cache_dict(event_data, self.data_cache.data.guilds[guild_id].soundboard_sounds, DataGuildCache.SoundboardSound, sound_id, overwrite=overwrite)

  def __update_soundboard_sounds(self, event_data: dict[str, Any], overwrite: bool=False):
    guild_id: str = event_data["guild_id"]
    sounds: list[dict[str, Any]] = event_data["soundboard_sounds"]
    super()._update_sync(sounds, self.data_cache.data.guilds[guild_id].soundboard_sounds, DataGuildCache.SoundboardSound, "sound_id", overwrite=overwrite)

  async def guild_create(self, event_data: dict[str, Any]):
    guild_id: str = event_data["id"]
    presences: list[dict[str, Any]] = event_data["presences"]
    voice_states: list[dict[str, Any]] = event_data["voice_states"]
    self.__update_guild_cache(event_data, guild_id)
    self.__connect_channel_thread_cache(guild_id)
    self.__update_voice_states(voice_states, guild_id)
    self.__update_presences(presences)

  async def guild_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["id"]
    self.__update_guild_cache(event_data, guild_id)

  async def guild_delete(self, event_data: dict[str, Any]):
    guild_id = event_data["id"]
    super()._delete_cache_dict(self.data_cache.data.guilds, guild_id)

  async def guild_audit_log_entry_create(self, event_data: dict[str, Any]):
    pass

  async def guild_ban_add(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user"]["id"]
    super()._add_cache_list(self.data_cache.data.guilds[guild_id].banned_users, user_id)

  async def guild_ban_remove(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user"]["id"]
    super()._delete_cache_list(self.data_cache.data.guilds[guild_id].banned_users, user_id)

  async def guild_emojis_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    emojis: list[dict[str, Any]] = event_data["emojis"]
    super()._update_sync(emojis, self.data_cache.data.guilds[guild_id].emojis, DataGuildCache.Emoji, "id")

  async def guild_stickers_update(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    stickers: list[dict[str, Any]] = event_data["stickers"]
    super()._update_sync(stickers, self.data_cache.data.guilds[guild_id].stickers, DataGuildCache.Sticker, "id")

  async def guild_integrations_update(self, event_data: dict[str, Any]):
    pass

  async def guild_member_add(self, event_data: dict[str, Any]):
    self.__update_guild_member(event_data)

  async def guild_member_remove(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user"]["id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].members, user_id)

  async def guild_member_update(self, event_data: dict[str, Any]):
    self.__update_guild_member(event_data)

  async def guild_members_chunk(self, event_data: dict[str, Any]):
    #TODO chunkの実装する
    guild_id: str = event_data["guild_id"]
    members: list[dict[str, Any]] = event_data["members"]
    presences: list[dict[str, Any]]|None = event_data.get("presences")
    super()._update_sync(members, self.data_cache.data.guilds[guild_id].members, DataGuildCache.GuildMember, "user.id")
    if presences is not None: self.__update_presences(presences)

  async def guild_role_create(self, event_data: dict[str, Any]):
    self.__update_guild_role(event_data, True)

  async def guild_role_update(self, event_data: dict[str, Any]):
    self.__update_guild_role(event_data)

  async def guild_role_delete(self, event_data: dict[str, Any]):
    guild_id = event_data["guild_id"]
    role_id = event_data["role_id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].roles, role_id)

  async def guild_scheduled_event_create(self, event_data: dict[str, Any]):
    self.__update_guild_scheduled_event(event_data, True)

  async def guild_scheduled_event_update(self, event_data: dict[str, Any]):
    self.__update_guild_scheduled_event(event_data)

  async def guild_scheduled_event_delete(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    event_id: str = event_data["id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].guild_scheduled_events, event_id)

  async def guild_scheduled_event_user_add(self, event_data: dict[str, Any]):
    event_id: str = event_data["guild_scheduled_event_id"]
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user_id"]
    super()._add_cache_list(self.data_cache.data.guilds[guild_id].guild_scheduled_events[event_id].users, user_id)

  async def guild_scheduled_event_user_remove(self, event_data: dict[str, Any]):
    event_id: str = event_data["guild_scheduled_event_id"]
    guild_id: str = event_data["guild_id"]
    user_id: str = event_data["user_id"]
    super()._delete_cache_list(self.data_cache.data.guilds[guild_id].guild_scheduled_events[event_id].users, user_id)

  async def guild_soundboard_sound_create(self, event_data: dict[str, Any]):
    self.__update_guild_soundboard_sound(event_data, True)

  async def guild_soundboard_sound_update(self, event_data: dict[str, Any]):
    self.__update_guild_soundboard_sound(event_data)

  async def guild_soundboard_sound_delete(self, event_data: dict[str, Any]):
    guild_id: str = event_data["guild_id"]
    sound_id: str = event_data["sound_id"]
    super()._delete_cache_dict(self.data_cache.data.guilds[guild_id].soundboard_sounds, sound_id)

  async def guild_soundboard_sounds_update(self, event_data: dict[str, Any]):
    self.__update_soundboard_sounds(event_data)

  async def soundboard_sounds(self, event_data: dict[str, Any]):
    self.__update_soundboard_sounds(event_data, True)