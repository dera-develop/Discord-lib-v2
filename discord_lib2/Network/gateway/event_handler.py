import asyncio
import json
from dacite import from_dict

from discord_lib2.logger import Logger
from discord_lib2.exception_catcher import ExceptionCatcher
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.user import guild as DataCacheGuild
from discord_lib2.cache.user import user as DataCacheUser
from discord_lib2.event import GatewayEvent
from discord_lib2.objects.resources import UserEventResources
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.gateway import request_payload
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.Network.gateway.websocket import WebsocketController
from discord_lib2.Network.http_request.http import HttpRequestController
from discord_lib2.Network.http_request.request_loader import RequestLoader

from discord_lib2.objects.gateway import recv_event_object

snowflake = str

class EventHandler:
  def __init__(
      self,
      logger: Logger,
      exception_catcher: ExceptionCatcher,
      system_cache_vault: SystemCacheVault,
      websocket_controller: WebsocketController,
      http_request_controller: HttpRequestController,
      user_event: GatewayEvent,
      http_request_loader: RequestLoader
  ) -> None:
    self.__task_event_handler = None
    self.logger = logger.get_child("GEH")
    self.cache_system = system_cache_vault
    self.cache_data = DataCacheVault()
    self.gateway_controller = websocket_controller
    self.exception_catcher = exception_catcher
    self.user_gateway_request = GatewayRequest(websocket_controller)
    self.user_http_request = HttpRequest(http_request_controller, http_request_loader)
    self.user_resources = UserEventResources(
      self.user_gateway_request,
      self.user_http_request,
      self.cache_data,
      logger
      )
    self.user_event_functions = user_event

    self.event_name_functions = {
      "READY": self.ready,
      "RESUMED": self.resumed,
      "GUILD_CREATE": self.guild_create,
      "GUILD_UPDATE": self.guild_update,
      "GUILD_DELETE": self.guild_delete,
      "GUILD_ROLE_CREATE": self.guild_role_create,
      "GUILD_ROLE_UPDATE": self.guild_role_update,
      "GUILD_ROLE_DELETE": self.guild_role_delete,
      "CHANNEL_CREATE": self.channel_create,
      "CHANNEL_UPDATE": self.channel_update,
      "CHANNEL_DELETE": self.channel_delete,
      "CHANNEL_PINS_UPDATE": self.channel_pins_update,
      "THREAD_CREATE": self.thread_create,
      "THREAD_UPDATE": self.thread_update,
      "THREAD_DELETE": self.thread_delete,
      "THREAD_LIST_SYNC": self.thread_list_sync,
      "THREAD_MEMBER_UPDATE": self.thread_member_update,
      "THREAD_MEMBERS_UPDATE": self.thread_members_update,
      "STAGE_INSTANCE_CREATE": self.stage_instance_create,
      "STAGE_INSTANCE_UPDATE": self.stage_instance_update,
      "STAGE_INSTANCE_DELETE": self.stage_instance_delete,
      "GUILD_MEMBER_ADD": self.guild_member_add,
      "GUILD_MEMBER_UPDATE": self.guild_member_update,
      "GUILD_MEMBERS_CHUNK": self.guild_members_chunk,
      "GUILD_MEMBER_REMOVE": self.guild_member_remove,
      "GUILD_AUDIT_LOG_ENTRY_CREATE": self.guild_audit_log_entry_create,
      "GUILD_BAN_ADD": self.guild_ban_add,
      "GUILD_BAN_REMOVE": self.guild_ban_remove,
      "GUILD_EMOJIS_UPDATE": self.guild_emojis_update,
      "GUILD_STICKERS_UPDATE": self.guild_stickers_update,
      "GUILD_SOUNDBOARD_SOUND_CREATE": self.guild_soundboard_sound_create,
      "GUILD_SOUNDBOARD_SOUND_UPDATE": self.guild_soundboard_sound_update,
      "GUILD_SOUNDBOARD_SOUND_DELETE": self.guild_soundboard_sound_delete,
      "GUILD_SOUNDBOARD_SOUNDS_UPDATE": self.guild_soundboard_sounds_update,
      "GUILD_INTEGRATIONS_UPDATE": self.guild_integrations_update,
      "INTEGRATION_CREATE": self.integration_create,
      "INTEGRATION_UPDATE": self.integration_update,
      "INTEGRATION_DELETE": self.integration_delete,
      "INTERACTION_CREATE": self.interaction_create,
      "WEBHOOKS_UPDATE": self.webhooks_update,
      "INVITE_CREATE": self.invite_create,
      "INVITE_DELETE": self.invite_delete,
      "VOICE_CHANNEL_EFFECT_SEND": self.voice_channel_effect_send,
      "VOICE_CHANNEL_START_TIME_UPDATE": self.voice_channel_start_time_update,
      "VOICE_CHANNEL_STATUS_UPDATE": self.voice_channel_status_update,
      "VOICE_SERVER_UPDATE": self.voice_server_update,
      "VOICE_STATE_UPDATE": self.voice_state_update,
      "PRESENCE_UPDATE": self.presence_update,
      "MESSAGE_CREATE": self.message_create,
      "MESSAGE_UPDATE": self.message_update,
      "MESSAGE_DELETE": self.message_delete,
      "MESSAGE_DELETE_BULK": self.message_delete_bulk,
      "MESSAGE_REACTION_ADD": self.message_reaction_add,
      "MESSAGE_REACTION_REMOVE": self.message_reaction_remove,
      "MESSAGE_REACTION_REMOVE_ALL": self.message_reaction_remove_all,
      "MESSAGE_REACTION_REMOVE_EMOJI": self.message_reaction_remove_emoji,
      "TYPING_START": self.typing_start,
      "USER_UPDATE": self.user_update,
      "GUILD_SCHEDULED_EVENT_CREATE": self.guild_scheduled_event_create,
      "GUILD_SCHEDULED_EVENT_UPDATE": self.guild_scheduled_event_update,
      "GUILD_SCHEDULED_EVENT_DELETE": self.guild_scheduled_event_delete,
      "GUILD_SCHEDULED_EVENT_USER_ADD": self.guild_scheduled_event_user_add,
      "GUILD_SCHEDULED_EVENT_USER_REMOVE": self.guild_scheduled_event_user_remove,
      "AUTO_MODERATION_RULE_CREATE": self.auto_moderation_rule_create,
      "AUTO_MODERATION_RULE_UPDATE": self.auto_moderation_rule_update,
      "AUTO_MODERATION_RULE_DELETE": self.auto_moderation_rule_delete,
      "AUTO_MODERATION_ACTION_EXECUTION": self.auto_moderation_action_execution,
      "MESSAGE_POLL_VOTE_ADD": self.message_poll_vote_add,
      "MESSAGE_POLL_VOTE_REMOVE": self.message_poll_vote_remove,
    }

  async def __worker_event_handler(self):
    try:
      self.logger.info("Task started | name: worker=event_handler")
      while True:
        dispatch_datas = str(await self.gateway_controller.get_event_queue())
        dispatch_dict = json.loads(dispatch_datas)
        event_name = dispatch_dict.get("t")
        event_data = dispatch_dict.get("d")
        await self.trigger(event_name, event_data)
    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  async def start(self):
    self.__task_event_handler = asyncio.create_task(self.__worker_event_handler())
  
  async def stop(self):
    if self.__task_event_handler is not None:
      if self.__task_event_handler:
        try:
          self.__task_event_handler.cancel()
          await self.__task_event_handler
        except:
          pass
        finally:
          self.logger.info(f"Task stopped | name=event_handler")

  async def trigger(self, event_name: str, event_data: dict):
    try:
      if event_name in self.event_name_functions:
        await self.event_name_functions[event_name](event_data)
      else:
        self.logger.warning(f"The event \"{event_name}\" has not been registered with the handler.")
    except Exception as e:
      self.logger.error(f"event process error | reason: {str(e)}")

########################################################################
## EVENT FUNCTIONS
########################################################################

  async def ready(self, event_data: dict):
    # system cache
    data_object = from_dict(recv_event_object.Ready, event_data)
    if isinstance(data_object.resume_gateway_url, str) and isinstance(data_object.session_id, str):
      self.cache_system.resume.reconnect_gateway_url = data_object.resume_gateway_url
      self.cache_system.resume.session_id = data_object.session_id
      self.cache_system.gateway.gateway_url = data_object.resume_gateway_url

    # data cache
    guilds = event_data.get("guilds")
    if isinstance(guilds, list):
      for guild in guilds:
        if isinstance(guild, dict):
          guild_id = guild.get("id")
          guild_unavailable = guild.get("unavailable")
          if not isinstance(guild_id, snowflake):
            continue
          if not isinstance(guild_unavailable, bool):
            continue
          self.cache_data.data.guilds[guild_id] = DataCacheGuild.GuildCache()
          self.cache_data.data.guilds[guild_id].id = guild_id
          self.cache_data.data.guilds[guild_id].unavailable = guild_unavailable
          if guild_unavailable:
            request_data = request_payload.RequestGuildMembers(guild_id, 0, "", True)
            await self.gateway_controller.send(request_data.get())

    await self.user_event_functions.ready(self.user_resources, data_object)

  async def resumed(self, event_data: dict):
    await self.user_event_functions.resumed(self.user_resources)

  async def guild_create(self, event_data: dict):
    guild_id = event_data.get("id")
    if isinstance(guild_id, snowflake):
      # guild cache
      ## guild
      if not guild_id in self.cache_data.data.guilds:
        self.cache_data.data.guilds[guild_id] = DataCacheGuild.GuildCache()
      self.cache_data.data.guilds[guild_id].update(event_data)
      ch_id_th_id: dict[snowflake, list[snowflake]] = {}
      for thread_id, data in self.cache_data.data.guilds[guild_id].threads.items():
        parent_ch = data.parent_id
        if parent_ch is not None:
          if not parent_ch in ch_id_th_id:
            ch_id_th_id[parent_ch] = []
          ch_id_th_id[parent_ch].append(thread_id)
      for k, v in ch_id_th_id.items():
        if k in self.cache_data.data.guilds[guild_id].channels:
          self.cache_data.data.guilds[guild_id].channels[k].threads = v
      ## member(voice state)
      voice_states = event_data.get("voice_states")
      if isinstance(voice_states, list):
        for voice_state in voice_states:
          if not isinstance(voice_state, dict):
            continue
          user_id = voice_state.get("user_id")
          if not isinstance(user_id, snowflake):
            continue
          if not user_id in self.cache_data.data.guilds[guild_id].members:
            self.cache_data.data.guilds[guild_id].members[user_id] = DataCacheGuild.GuildMember()
          self.cache_data.data.guilds[guild_id].members[user_id].voice_state.update(voice_state)
      # user cache
      ## presence
      presences = event_data.get("presences")
      if isinstance(presences, list):
        for presence in presences:
          if not isinstance(presence, dict):
            continue
          user_id = presence.get("user")
          if not isinstance(user_id, dict):
            continue
          user_id = user_id.get("id")
          if not isinstance(user_id, snowflake):
            continue
          if not user_id in self.cache_data.data.users:
            self.cache_data.data.users[user_id] = DataCacheUser.User()
          self.cache_data.data.users[user_id].presence.update(presence)
    data_object = from_dict(recv_event_object.GuildCreate, event_data)
    await self.user_event_functions.guild_create(self.user_resources, data_object)

  async def guild_update(self, event_data: dict):
    guild_id = event_data.get("id")
    if isinstance(guild_id, snowflake):
      if not guild_id in self.cache_data.data.guilds:
        self.cache_data.data.guilds[guild_id] = DataCacheGuild.GuildCache()
        request_data = request_payload.RequestGuildMembers(guild_id, 0, "", True)
        await self.gateway_controller.send(request_data.get())
      self.cache_data.data.guilds[guild_id].update(event_data)
    data_object = from_dict(recv_event_object.Guild, event_data)
    await self.user_event_functions.guild_update(self.user_resources, data_object)

  async def guild_delete(self, event_data: dict):
    guild_id = event_data.get("id")
    if isinstance(guild_id, snowflake):
      if guild_id in self.cache_data.data.guilds:
        self.cache_data.data.guilds.pop(guild_id)
    data_object = from_dict(recv_event_object.Guild, event_data)
    await self.user_event_functions.guild_delete(self.user_resources, data_object)

  async def guild_role_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    if not isinstance(guild_id, snowflake):
      return
    role_data = event_data.get("roles")
    if isinstance(role_data, dict):
      role_id = role_data.get("id")
      if isinstance(role_id, snowflake):
        self.cache_data.data.guilds[guild_id].roles[role_id] = DataCacheGuild.Role()
        self.cache_data.data.guilds[guild_id].roles[role_id].update(role_data)
    data_object = from_dict(recv_event_object.GuildRoleEvent, event_data)
    await self.user_event_functions.guild_role_create(self.user_resources, data_object)

  async def guild_role_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    if not isinstance(guild_id, snowflake):
      return
    role_data = event_data.get("roles")
    if isinstance(role_data, dict):
      role_id = role_data.get("id")
      if isinstance(role_id, snowflake):
        if not role_id in self.cache_data.data.guilds[guild_id].roles:
          self.cache_data.data.guilds[guild_id].roles[role_id] = DataCacheGuild.Role()
        self.cache_data.data.guilds[guild_id].roles[role_id].update(role_data)
    data_object = from_dict(recv_event_object.GuildRoleEvent, event_data)
    await self.user_event_functions.guild_role_update(self.user_resources, data_object)

  async def guild_role_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    role_id = event_data.get("role_id")
    if isinstance(guild_id, snowflake) and isinstance(role_id, snowflake):
      if role_id in self.cache_data.data.guilds[guild_id].roles:
        self.cache_data.data.guilds[guild_id].roles.pop(role_id)
    data_object = from_dict(recv_event_object.GuildRoleDelete, event_data)  
    await self.user_event_functions.guild_role_delete(self.user_resources, data_object)

  async def channel_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    channel_id = event_data.get("channel_id")
    if isinstance(guild_id, snowflake) and isinstance(channel_id, snowflake):
      self.cache_data.data.guilds[guild_id].channels[channel_id] = DataCacheGuild.Channel()
      self.cache_data.data.guilds[guild_id].channels[channel_id].update(event_data)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.channel_create(self.user_resources, data_object)

  async def channel_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    channel_id = event_data.get("channel_id")
    if isinstance(guild_id, snowflake) and isinstance(channel_id, snowflake):
      if not channel_id in self.cache_data.data.guilds[guild_id].channels:
        self.cache_data.data.guilds[guild_id].channels[channel_id] = DataCacheGuild.Channel()
      self.cache_data.data.guilds[guild_id].channels[channel_id].update(event_data)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.channel_update(self.user_resources, data_object)

  async def channel_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    channel_id = event_data.get("channel_id")
    if isinstance(guild_id, snowflake) and isinstance(channel_id, snowflake):
      if channel_id in self.cache_data.data.guilds[guild_id].channels:
        self.cache_data.data.guilds[guild_id].channels.pop(channel_id)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.channel_delete(self.user_resources, data_object)

  async def channel_pins_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.ChannelPinsUpdate, event_data)
    await self.user_event_functions.channel_pins_update(self.user_resources, data_object)

  async def thread_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    thread_id = event_data.get("channel_id")
    newly_created = event_data.pop("newly_created", False)
    if isinstance(guild_id, snowflake) and isinstance(thread_id, snowflake):
      self.cache_data.data.guilds[guild_id].threads[thread_id] = DataCacheGuild.Thread()
      self.cache_data.data.guilds[guild_id].threads[thread_id].update(event_data)
      parent_id = event_data.get("parent_id")
      if parent_id is not None and parent_id in self.cache_data.data.guilds[guild_id].channels:
        self.cache_data.data.guilds[guild_id].channels[parent_id].threads.append(thread_id)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.thread_create(self.user_resources, newly_created, data_object)

  async def thread_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    thread_id = event_data.get("channel_id")
    if isinstance(guild_id, snowflake) and isinstance(thread_id, snowflake):
      if not thread_id in self.cache_data.data.guilds[guild_id].threads:
        self.cache_data.data.guilds[guild_id].threads[thread_id] = DataCacheGuild.Thread()
        parent_id = event_data.get("parent_id")
        if parent_id is not None and parent_id in self.cache_data.data.guilds[guild_id].channels:
          self.cache_data.data.guilds[guild_id].channels[parent_id].threads.append(thread_id)
      self.cache_data.data.guilds[guild_id].threads[thread_id].update(event_data)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.thread_update(self.user_resources, data_object)

  async def thread_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    thread_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(thread_id, snowflake):
      if thread_id in self.cache_data.data.guilds[guild_id].threads:
        parent_id = self.cache_data.data.guilds[guild_id].threads[thread_id].parent_id
        if isinstance(parent_id, snowflake) and isinstance(thread_id, snowflake):
          self.cache_data.data.guilds[guild_id].channels[parent_id].threads.remove(thread_id)
        self.cache_data.data.guilds[guild_id].threads.pop(thread_id)
    data_object = from_dict(recv_event_object.Channel, event_data)
    await self.user_event_functions.thread_delete(self.user_resources, data_object)

  async def thread_list_sync(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    channel_ids = event_data.get("channel_ids")
    if isinstance(channel_ids, list) and isinstance(guild_id, snowflake):
      for channel_id in channel_ids:
        delete_thread = list(self.cache_data.data.guilds[guild_id].channels[channel_id].threads)
        for thread_id in delete_thread:
          self.cache_data.data.guilds[guild_id].threads.pop(thread_id)
        self.cache_data.data.guilds[guild_id].channels[channel_id].threads = []
      threads = event_data.get("threads")
      if isinstance(threads, list):
        for thread in threads:
          if isinstance(thread, dict):
            ### thread create
            thread_id = thread.get("channel_id")
            if isinstance(thread_id, snowflake):
              self.cache_data.data.guilds[guild_id].threads[thread_id] = DataCacheGuild.Thread()
              self.cache_data.data.guilds[guild_id].threads[thread_id].update(thread)
              parent_id = thread.get("parent_id")
              if parent_id is not None and parent_id in self.cache_data.data.guilds[guild_id].channels:
                self.cache_data.data.guilds[guild_id].channels[parent_id].threads.append(thread_id)
            ###
      members = event_data.get("members")
      if isinstance(members, list):
        for member in members:
          if isinstance(member, dict):
            join_thread_id = member.get("id")
            user_id = member.get("user_id")
            if isinstance(join_thread_id, snowflake) and isinstance(user_id, snowflake):
              self.cache_data.data.guilds[guild_id].threads[join_thread_id].members[user_id] = DataCacheGuild.ThreadMember()
              self.cache_data.data.guilds[guild_id].threads[join_thread_id].members[user_id].update(member)
    data_object = from_dict(recv_event_object.ThreadListSync, event_data)
    await self.user_event_functions.thread_list_sync(self.user_resources, data_object)

  async def thread_member_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    thread_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(thread_id, snowflake):
      self.cache_data.data.guilds[guild_id].threads[thread_id].member.update(event_data)
    data_object = from_dict(recv_event_object.Channel.ThreadMember, event_data)
    await self.user_event_functions.thread_member_update(self.user_resources, data_object)

  async def thread_members_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    thread_id = event_data.get("id")
    member_count = event_data.get("member_count")
    added_members = event_data.get("added_members")
    removed_member_ids = event_data.get("removed_member_ids")
    if isinstance(guild_id, snowflake) and isinstance(thread_id, snowflake) and isinstance(member_count, int) and isinstance(added_members, list) and isinstance(removed_member_ids, list):
      for removed_member_id in removed_member_ids:
        if removed_member_id in self.cache_data.data.guilds[guild_id].members:
          self.cache_data.data.guilds[guild_id].threads[thread_id].members.pop(removed_member_id)
      for added_member in added_members:
        if isinstance(added_member, dict):
          user_id = added_member.get("user_id")
          if isinstance(user_id, snowflake):
            self.cache_data.data.guilds[guild_id].threads[thread_id].members[user_id].update(added_member)
      self.cache_data.data.guilds[guild_id].threads[thread_id].member_count = member_count
    data_object = from_dict(recv_event_object.ThreadMembersUpdate, event_data)
    await self.user_event_functions.thread_members_update(self.user_resources, data_object)

  async def stage_instance_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    stage_instance_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(stage_instance_id, snowflake):
      self.cache_data.data.guilds[guild_id].stage_instances[stage_instance_id] = DataCacheGuild.StageInstance()
      self.cache_data.data.guilds[guild_id].stage_instances[stage_instance_id].update(event_data)
    data_object = from_dict(recv_event_object.StageInstance, event_data)
    await self.user_event_functions.stage_instance_create(self.user_resources, data_object)

  async def stage_instance_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    stage_instance_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(stage_instance_id, snowflake):
      if not stage_instance_id in self.cache_data.data.guilds[guild_id].stage_instances:
        self.cache_data.data.guilds[guild_id].stage_instances[stage_instance_id] = DataCacheGuild.StageInstance()
      self.cache_data.data.guilds[guild_id].stage_instances[stage_instance_id].update(event_data)
    data_object = from_dict(recv_event_object.StageInstance, event_data)
    await self.user_event_functions.stage_instance_update(self.user_resources, data_object)

  async def stage_instance_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    stage_instance_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(stage_instance_id, snowflake):
      if stage_instance_id in self.cache_data.data.guilds[guild_id].stage_instances:
        self.cache_data.data.guilds[guild_id].stage_instances.pop(stage_instance_id)
    data_object = from_dict(recv_event_object.StageInstance, event_data)
    await self.user_event_functions.stage_instance_delete(self.user_resources, data_object)

  async def guild_member_add(self, event_data: dict):
    new = True  # new member flag
    guild_id = event_data.get("guild_id")
    user_id = event_data.get("user")
    joined_at = event_data.get("joined_at")
    if isinstance(user_id, dict):
      user_id = user_id.get("id")
    if isinstance(guild_id, snowflake) and isinstance(user_id, snowflake) and isinstance(joined_at, str):
      # new member check
      if user_id in self.cache_data.data.guilds[guild_id].members:
        if self.cache_data.data.guilds[guild_id].members[user_id].joined_at == joined_at:
          new = False
      # # # # # # # # #
      self.cache_data.data.guilds[guild_id].members[user_id] = DataCacheGuild.GuildMember()
      self.cache_data.data.guilds[guild_id].members[user_id].update(event_data)
      data_object = from_dict(recv_event_object.GuildMemberAdd, event_data)
      await self.user_event_functions.guild_member_add(self.user_resources, new, data_object)

  async def guild_member_update(self, event_data: dict):
    guild_id = event_data.pop("guild_id", None)
    user_id = event_data.get("user")
    if isinstance(user_id, dict):
      user_id = user_id.get("id")
    if isinstance(guild_id, snowflake) and isinstance(user_id, snowflake):
      if not user_id in self.cache_data.data.guilds[guild_id].members:
        self.cache_data.data.guilds[guild_id].members[user_id] = DataCacheGuild.GuildMember()
      self.cache_data.data.guilds[guild_id].members[user_id].update(event_data)
    data_object = from_dict(recv_event_object.GuildMemberUpdate, event_data)
    await self.user_event_functions.guild_member_update(self.user_resources, data_object)

  #TODO chunkを扱うようにするか否か
  async def guild_members_chunk(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    members = event_data.get("members")
    chunk_index = event_data.get("chunk_index")
    chunk_count = event_data.get("chunk_count")
    not_found = event_data.get("not_found")
    presences = event_data.get("presences")
    nonce = event_data.get("nonce")
    if isinstance(guild_id, snowflake):
      # guild members
      if isinstance(members, list):
        for member in members:
          if not isinstance(member, dict):
            continue
          user_id = member.get("user")
          if not isinstance(user_id, dict):
            continue
          user_id = user_id.get("id")
          if not isinstance(user_id, snowflake):
            continue
          if not user_id in self.cache_data.data.guilds[guild_id].members:
            self.cache_data.data.guilds[guild_id].members[user_id] = DataCacheGuild.GuildMember()
          self.cache_data.data.guilds[guild_id].members[user_id].update(member)
      # presences
      if isinstance(presences, list):
        for presence in presences:
          if not isinstance(presence, dict):
            continue
          user_id = presence.get("user")
          if not isinstance(user_id, dict):
            continue
          user_id = user_id.get("id")
          if not isinstance(user_id, snowflake):
            continue
          if not user_id in self.cache_data.data.users:
            self.cache_data.data.users[user_id] = DataCacheUser.User()
          self.cache_data.data.users[user_id].presence.update(presence)
    data_object = from_dict(recv_event_object.GuildMembersChunk, event_data)
    await self.user_event_functions.guild_members_chunk(self.user_resources, data_object)

  async def guild_member_remove(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    user_id = event_data.get("user")
    if isinstance(user_id, dict):
      user_id = user_id.get("id")
    if isinstance(guild_id, snowflake) and isinstance(user_id, snowflake):
      if user_id in self.cache_data.data.guilds[guild_id].members:
        self.cache_data.data.guilds[guild_id].members.pop(user_id)
      if user_id in self.cache_data.data.users:
        if guild_id in self.cache_data.data.users[user_id].joined_guilds:
          self.cache_data.data.users[user_id].joined_guilds.remove(guild_id)
          if len(self.cache_data.data.users[user_id].joined_guilds) == 0:
            self.cache_data.data.users.pop(user_id)
    data_object = from_dict(recv_event_object.GuildMemberRemove, event_data)
    await self.user_event_functions.guild_member_remove(self.user_resources, data_object)

  async def guild_audit_log_entry_create(self, event_data: dict):
    await self.user_event_functions.guild_audit_log_entry_create(self.user_resources)

  async def guild_ban_add(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    user_id = event_data.get("user")
    if isinstance(guild_id, snowflake) and isinstance(user_id, dict):
      user_id = user_id.get("id")
      if isinstance(user_id, snowflake):
        self.cache_data.data.guilds[guild_id].banned_users.append(user_id)
    data_object = from_dict(recv_event_object.GuildBanEvent, event_data)
    await self.user_event_functions.guild_ban_add(self.user_resources, data_object)

  async def guild_ban_remove(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    user_id = event_data.get("user")
    if isinstance(guild_id, snowflake) and isinstance(user_id, dict):
      user_id = user_id.get("id")
      if isinstance(user_id, snowflake):
        if user_id in self.cache_data.data.guilds[guild_id].banned_users:
          self.cache_data.data.guilds[guild_id].banned_users.remove(user_id)
    data_object = from_dict(recv_event_object.GuildBanEvent, event_data)
    await self.user_event_functions.guild_ban_remove(self.user_resources, data_object)

  async def guild_emojis_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    emojis = event_data.get("emojis")
    if isinstance(guild_id, snowflake) and isinstance(emojis, list):
      for emoji in emojis:
        if not isinstance(emoji, dict):
          continue
        emoji_id = emoji.get("id")
        if not isinstance(emoji_id, snowflake):
          continue
        if not emoji_id in self.cache_data.data.guilds[guild_id].emojis:
          self.cache_data.data.guilds[guild_id].emojis[emoji_id] = DataCacheGuild.Emoji()
        self.cache_data.data.guilds[guild_id].emojis[emoji_id].update(emoji)
    data_object = from_dict(recv_event_object.GuildEmojisUpdate, event_data)
    await self.user_event_functions.guild_emojis_update(self.user_resources, data_object)

  async def guild_stickers_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    stickers = event_data.get("stickers")
    if isinstance(guild_id, snowflake) and isinstance(stickers, list):
      for sticker in stickers:
        if not isinstance(sticker, dict):
          continue
        sticker_id = sticker.get("id")
        if not isinstance(sticker_id, snowflake):
          continue
        if not sticker_id in self.cache_data.data.guilds[guild_id].stickers:
          self.cache_data.data.guilds[guild_id].stickers[sticker_id] = DataCacheGuild.Sticker()
        self.cache_data.data.guilds[guild_id].stickers[sticker_id].update(sticker)
    data_object = from_dict(recv_event_object.GuildStickersUpdate, event_data)
    await self.user_event_functions.guild_stickers_update(self.user_resources, data_object)

  async def guild_soundboard_sound_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    sound_id = event_data.get("sound_id")
    if isinstance(guild_id, snowflake) and isinstance(sound_id, snowflake):
      self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id] = DataCacheGuild.SoundboardSound()
      self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id].update(event_data)
    data_object = from_dict(recv_event_object.SoundboardSound, event_data)
    await self.user_event_functions.guild_soundboard_sound_create(self.user_resources, data_object)

  async def guild_soundboard_sound_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    sound_id = event_data.get("sound_id")
    if isinstance(guild_id, snowflake) and isinstance(sound_id, snowflake):
      if not sound_id in self.cache_data.data.guilds[guild_id].soundboard_sounds:
        self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id] = DataCacheGuild.SoundboardSound()
      self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id].update(event_data)
    data_object = from_dict(recv_event_object.SoundboardSound, event_data)
    await self.user_event_functions.guild_soundboard_sound_update(self.user_resources, data_object)

  async def guild_soundboard_sound_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    sound_id = event_data.get("sound_id")
    if isinstance(guild_id, snowflake) and isinstance(sound_id, snowflake):
      if sound_id in self.cache_data.data.guilds[guild_id].soundboard_sounds:
        self.cache_data.data.guilds[guild_id].soundboard_sounds.pop(sound_id)
    data_object = from_dict(recv_event_object.GuildSoundboardSoundDelete, event_data)
    await self.user_event_functions.guild_soundboard_sound_delete(self.user_resources, data_object)

  async def guild_soundboard_sounds_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    soundboard_sounds = event_data.get("soundboard_sounds")
    if isinstance(guild_id, snowflake) and isinstance(soundboard_sounds, list):
      for soundboard_sound in soundboard_sounds:
        sound_id = event_data.get("sound_id")
        if isinstance(sound_id, snowflake):
          if not sound_id in self.cache_data.data.guilds[guild_id].soundboard_sounds:
            self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id] = DataCacheGuild.SoundboardSound()
          self.cache_data.data.guilds[guild_id].soundboard_sounds[sound_id].update(soundboard_sound)
    data_object = from_dict(recv_event_object.GuildSoundboardSoundsUpdate, event_data)
    await self.user_event_functions.guild_soundboard_sounds_update(self.user_resources, data_object)

  async def guild_integrations_update(self, event_data: dict):
    await self.user_event_functions.guild_integrations_update(self.user_resources)

  async def integration_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    integration_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(integration_id, snowflake):
      self.cache_data.data.guilds[guild_id].integrations[integration_id] = DataCacheGuild.Integration()
      self.cache_data.data.guilds[guild_id].integrations.update(event_data)
    data_object = from_dict(recv_event_object.IntegrationEvent, event_data)
    await self.user_event_functions.integration_create(self.user_resources, data_object)

  async def integration_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    integration_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(integration_id, snowflake):
      if not integration_id in self.cache_data.data.guilds[guild_id].integrations:
        self.cache_data.data.guilds[guild_id].integrations[integration_id] = DataCacheGuild.Integration()
      self.cache_data.data.guilds[guild_id].integrations.update(event_data)
    data_object = from_dict(recv_event_object.IntegrationEvent, event_data)
    await self.user_event_functions.integration_update(self.user_resources, data_object)

  async def integration_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    integration_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(integration_id, snowflake):
      if integration_id in self.cache_data.data.guilds[guild_id].integrations:
        self.cache_data.data.guilds[guild_id].integrations.pop(integration_id)
    data_object = from_dict(recv_event_object.IntegrationDelete, event_data)
    await self.user_event_functions.integration_delete(self.user_resources, data_object)

  async def interaction_create(self, event_data: dict):
    data_object = from_dict(recv_event_object.Interaction, event_data)
    await self.user_event_functions.interaction_create(self.user_resources, data_object)

  async def webhooks_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.WebhooksUpdate, event_data)
    await self.user_event_functions.webhooks_update(self.user_resources, data_object)

  async def invite_create(self, event_data: dict):
    data_object = from_dict(recv_event_object.InviteCreate, event_data)
    await self.user_event_functions.invite_create(self.user_resources, data_object)

  async def invite_delete(self, event_data: dict):
    data_object = from_dict(recv_event_object.InviteDelete, event_data)
    await self.user_event_functions.invite_delete(self.user_resources, data_object)

  async def voice_channel_effect_send(self, event_data: dict):
    data_object = from_dict(recv_event_object.VoiceChannelEffectSend, event_data)
    await self.user_event_functions.voice_channel_effect_send(self.user_resources, data_object)

  async def voice_channel_start_time_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.VoiceChannelStartTimeUpdate, event_data)
    await self.user_event_functions.voice_channel_start_time_update(self.user_resources, data_object)

  async def voice_channel_status_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.VoiceChannelStatusUpdate, event_data)
    await self.user_event_functions.voice_channel_status_update(self.user_resources, data_object)

  async def voice_server_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.VoiceServerUpdate, event_data)
    await self.user_event_functions.voice_server_update(self.user_resources, data_object)

  async def voice_state_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    user_id = event_data.get("user_id")
    if isinstance(guild_id, snowflake) and isinstance(user_id, snowflake):
      if not user_id in self.cache_data.data.guilds[guild_id].members:
        self.cache_data.data.guilds[guild_id].members[user_id] = DataCacheGuild.GuildMember()
      self.cache_data.data.guilds[guild_id].members[user_id].voice_state.update(event_data)
    data_object = from_dict(recv_event_object.VoiceState, event_data)
    await self.user_event_functions.voice_state_update(self.user_resources, data_object)

  async def presence_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.PresenceUpdate, event_data)
    await self.user_event_functions.presence_update(self.user_resources, data_object)

  async def message_create(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageCreateUpdate, event_data)
    await self.user_event_functions.message_create(self.user_resources, data_object)

  async def message_update(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageCreateUpdate, event_data)
    await self.user_event_functions.message_update(self.user_resources, data_object)

  async def message_delete(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageDelete, event_data)
    await self.user_event_functions.message_delete(self.user_resources, data_object)

  async def message_delete_bulk(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageDeleteBulk, event_data)
    await self.user_event_functions.message_delete_bulk(self.user_resources, data_object)

  async def message_reaction_add(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageReactionAdd, event_data)
    await self.user_event_functions.message_reaction_add(self.user_resources, data_object)

  async def message_reaction_remove(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageReactionRemove, event_data)
    await self.user_event_functions.message_reaction_remove(self.user_resources, data_object)

  async def message_reaction_remove_all(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageReactionRemoveAll, event_data)
    await self.user_event_functions.message_reaction_remove_all(self.user_resources, data_object)

  async def message_reaction_remove_emoji(self, event_data: dict):
    data_object = from_dict(recv_event_object.MessageReactionRemoveEmoji, event_data)
    await self.user_event_functions.message_reaction_remove_emoji(self.user_resources, data_object)

  async def typing_start(self, event_data: dict):
    data_object = from_dict(recv_event_object.TypingStart, event_data)
    await self.user_event_functions.typing_start(self.user_resources, data_object)

  async def user_update(self, event_data: dict):
    user_id = event_data.get("id")
    if isinstance(user_id, snowflake):
      if not user_id in self.cache_data.data.users:
        self.cache_data.data.users[user_id] = DataCacheUser.User()
      self.cache_data.data.users[user_id].update(event_data)
    data_object = from_dict(recv_event_object.User, event_data)
    await self.user_event_functions.user_update(self.user_resources, data_object)

  async def guild_scheduled_event_create(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    event_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(event_id, snowflake):
      self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id] = DataCacheGuild.GuildScheduledEvent()
      self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id].update(event_data)
    data_object = from_dict(recv_event_object.GuildScheduledEvent, event_data)
    await self.user_event_functions.guild_scheduled_event_create(self.user_resources, data_object)

  async def guild_scheduled_event_update(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    event_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(event_id, snowflake):
      if not event_id in self.cache_data.data.guilds[guild_id].guild_scheduled_events:
        self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id] = DataCacheGuild.GuildScheduledEvent()
      self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id].update(event_data)
    data_object = from_dict(recv_event_object.GuildScheduledEvent, event_data)
    await self.user_event_functions.guild_scheduled_event_update(self.user_resources, data_object)

  async def guild_scheduled_event_delete(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    event_id = event_data.get("id")
    if isinstance(guild_id, snowflake) and isinstance(event_id, snowflake):
      if event_id in self.cache_data.data.guilds[guild_id].guild_scheduled_events:
        self.cache_data.data.guilds[guild_id].guild_scheduled_events.pop(event_id)
    data_object = from_dict(recv_event_object.GuildScheduledEvent, event_data)
    await self.user_event_functions.guild_scheduled_event_delete(self.user_resources, data_object)

  async def guild_scheduled_event_user_add(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    event_id = event_data.get("guild_scheduled_event_id")
    user_id = event_data.get("user_id")
    if isinstance(guild_id, snowflake) and isinstance(event_id, snowflake) and isinstance(user_id, snowflake):
      if event_id in self.cache_data.data.guilds[guild_id].guild_scheduled_events:
        self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id].users.append(user_id)
    data_object = from_dict(recv_event_object.GuildScheduledEventUserAdd, event_data)
    await self.user_event_functions.guild_scheduled_event_user_add(self.user_resources, data_object)

  async def guild_scheduled_event_user_remove(self, event_data: dict):
    guild_id = event_data.get("guild_id")
    event_id = event_data.get("guild_scheduled_event_id")
    user_id = event_data.get("user_id")
    if isinstance(guild_id, snowflake) and isinstance(event_id, snowflake) and isinstance(user_id, snowflake):
      if event_id in self.cache_data.data.guilds[guild_id].guild_scheduled_events:
        if user_id in self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id].users:
          self.cache_data.data.guilds[guild_id].guild_scheduled_events[event_id].users.remove(user_id)
    data_object = from_dict(recv_event_object.GuildScheduledEventUserRemove, event_data)
    await self.user_event_functions.guild_scheduled_event_user_remove(self.user_resources, data_object)

  async def auto_moderation_rule_create(self, event_data: dict):
    await self.user_event_functions.auto_moderation_rule_create(self.user_resources)

  async def auto_moderation_rule_update(self, event_data: dict):
    await self.user_event_functions.auto_moderation_rule_update(self.user_resources)

  async def auto_moderation_rule_delete(self, event_data: dict):
    await self.user_event_functions.auto_moderation_rule_delete(self.user_resources)

  async def auto_moderation_action_execution(self, event_data: dict):
    await self.user_event_functions.auto_moderation_action_execution(self.user_resources)

  async def message_poll_vote_add(self, event_data: dict):
    await self.user_event_functions.message_poll_vote_add(self.user_resources)

  async def message_poll_vote_remove(self, event_data: dict):
    await self.user_event_functions.message_poll_vote_remove(self.user_resources)