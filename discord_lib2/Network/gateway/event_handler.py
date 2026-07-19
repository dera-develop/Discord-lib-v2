import asyncio
import json

from discord_lib2.logger import Logger
from discord_lib2.exception_catcher import ExceptionCatcher
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.cache.user import DataCacheVault
from discord_lib2.cache.onetime import OnetimeCacheVault
from discord_lib2.Network.gateway.websocket import WebsocketController
from discord_lib2.Network.http_request.http import HttpRequestController
from discord_lib2.event import GatewayEvent
from discord_lib2.objects.resources import UserEventResources
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.Network.http_request.request_loader import RequestLoader

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
    self.logger = logger.get_child("EHL")
    self.cache_system = system_cache_vault
    self.cache_user = DataCacheVault()
    self.cache_onetime = OnetimeCacheVault()
    self.gateway_controller = websocket_controller
    self.exception_catcher = exception_catcher
    self.user_gateway_request = GatewayRequest(websocket_controller)
    self.user_http_request = HttpRequest(http_request_controller, http_request_loader)
    self.user_resources = UserEventResources(
      self.user_gateway_request,
      self.user_http_request,
      self.cache_user,
      self.cache_onetime
      )
    self.user_event_functions = user_event

    self.event_name_functions = {
      'READY': self.ready,
      'RESUMED': self.resumed,
      'GUILD_CREATE': self.guild_create,
      'GUILD_UPDATE': self.guild_update,
      'GUILD_DELETE': self.guild_delete,
      'GUILD_ROLE_CREATE': self.guild_role_create,
      'GUILD_ROLE_UPDATE': self.guild_role_update,
      'GUILD_ROLE_DELETE': self.guild_role_delete,
      'CHANNEL_CREATE': self.channel_create,
      'CHANNEL_UPDATE': self.channel_update,
      'CHANNEL_DELETE': self.channel_delete,
      'CHANNEL_PINS_UPDATE': self.channel_pins_update,
      'THREAD_CREATE': self.thread_create,
      'THREAD_UPDATE': self.thread_update,
      'THREAD_DELETE': self.thread_delete,
      'THREAD_LIST_SYNC': self.thread_list_sync,
      'THREAD_MEMBER_UPDATE': self.thread_member_update,
      'THREAD_MEMBERS_UPDATE': self.thread_members_update,
      'STAGE_INSTANCE_CREATE': self.stage_instance_create,
      'STAGE_INSTANCE_UPDATE': self.stage_instance_update,
      'STAGE_INSTANCE_DELETE': self.stage_instance_delete,
      'GUILD_MEMBER_ADD': self.guild_member_add,
      'GUILD_MEMBER_UPDATE': self.guild_member_update,
      'GUILD_MEMBERS_CHUNK': self.guild_members_chunk,
      'GUILD_MEMBER_REMOVE': self.guild_member_remove,
      'GUILD_AUDIT_LOG_ENTRY_CREATE': self.guild_audit_log_entry_create,
      'GUILD_BAN_ADD': self.guild_ban_add,
      'GUILD_BAN_REMOVE': self.guild_ban_remove,
      'GUILD_EMOJIS_UPDATE': self.guild_emojis_update,
      'GUILD_STICKERS_UPDATE': self.guild_stickers_update,
      'GUILD_SOUNDBOARD_SOUND_CREATE': self.guild_soundboard_sound_create,
      'GUILD_SOUNDBOARD_SOUND_UPDATE': self.guild_soundboard_sound_update,
      'GUILD_SOUNDBOARD_SOUND_DELETE': self.guild_soundboard_sound_delete,
      'GUILD_SOUNDBOARD_SOUNDS_UPDATE': self.guild_soundboard_sounds_update,
      'GUILD_INTEGRATIONS_UPDATE': self.guild_integrations_update,
      'INTEGRATION_CREATE': self.integration_create,
      'INTEGRATION_UPDATE': self.integration_update,
      'INTEGRATION_DELETE': self.integration_delete,
      'INTERACTION_CREATE': self.interaction_create,
      'WEBHOOKS_UPDATE': self.webhooks_update,
      'INVITE_CREATE': self.invite_create,
      'INVITE_DELETE': self.invite_delete,
      'VOICE_CHANNEL_EFFECT_SEND': self.voice_channel_effect_send,
      'VOICE_STATE_UPDATE': self.voice_state_update,
      'PRESENCE_UPDATE': self.presence_update,
      'MESSAGE_CREATE': self.message_create,
      'MESSAGE_UPDATE': self.message_update,
      'MESSAGE_DELETE': self.message_delete,
      'MESSAGE_DELETE_BULK': self.message_delete_bulk,
      'MESSAGE_REACTION_ADD': self.message_reaction_add,
      'MESSAGE_REACTION_REMOVE': self.message_reaction_remove,
      'MESSAGE_REACTION_REMOVE_ALL': self.message_reaction_remove_all,
      'MESSAGE_REACTION_REMOVE_EMOJI': self.message_reaction_remove_emoji,
      'TYPING_START': self.typing_start,
      'USER_UPDATE': self.user_update,
      'GUILD_SCHEDULED_EVENT_CREATE': self.guild_scheduled_event_create,
      'GUILD_SCHEDULED_EVENT_UPDATE': self.guild_scheduled_event_update,
      'GUILD_SCHEDULED_EVENT_DELETE': self.guild_scheduled_event_delete,
      'GUILD_SCHEDULED_EVENT_USER_ADD': self.guild_scheduled_event_user_add,
      'GUILD_SCHEDULED_EVENT_USER_REMOVE': self.guild_scheduled_event_user_remove,
      'AUTO_MODERATION_RULE_CREATE': self.auto_moderation_rule_create,
      'AUTO_MODERATION_RULE_UPDATE': self.auto_moderation_rule_update,
      'AUTO_MODERATION_RULE_DELETE': self.auto_moderation_rule_delete,
      'AUTO_MODERATION_ACTION_EXECUTION': self.auto_moderation_action_execution,
      'MESSAGE_POLL_VOTE_ADD': self.message_poll_vote_add,
      'MESSAGE_POLL_VOTE_REMOVE': self.message_poll_vote_remove,
    }

  async def __worker_event_handler(self):
    try:
      self.logger.info("Task started | name: worker=event_handler")
      while True:
        dispatch_datas = str(await self.gateway_controller.get_event_queue())
        dispatch_dict = json.loads(dispatch_datas)
        event_name = dispatch_dict.get("t")
        event_data = dispatch_dict.get("d")
        await self.event_name_functions[event_name](event_data)
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

  async def ready(self, event_data: dict):
    await self.user_event_functions.ready(self.user_resources)

  async def resumed(self, event_data: dict):
    await self.user_event_functions.resumed(self.user_resources)

  async def guild_create(self, event_data: dict):
    await self.user_event_functions.guild_create(self.user_resources)

  async def guild_update(self, event_data: dict):
    await self.user_event_functions.guild_update(self.user_resources)

  async def guild_delete(self, event_data: dict):
    await self.user_event_functions.guild_delete(self.user_resources)

  async def guild_role_create(self, event_data: dict):
    await self.user_event_functions.guild_role_create(self.user_resources)

  async def guild_role_update(self, event_data: dict):
    await self.user_event_functions.guild_role_update(self.user_resources)

  async def guild_role_delete(self, event_data: dict):
    await self.user_event_functions.guild_role_delete(self.user_resources)

  async def channel_create(self, event_data: dict):
    await self.user_event_functions.channel_create(self.user_resources)

  async def channel_update(self, event_data: dict):
    await self.user_event_functions.channel_update(self.user_resources)

  async def channel_delete(self, event_data: dict):
    await self.user_event_functions.channel_delete(self.user_resources)

  async def channel_pins_update(self, event_data: dict):
    await self.user_event_functions.channel_pins_update(self.user_resources)

  async def thread_create(self, event_data: dict):
    await self.user_event_functions.thread_create(self.user_resources)

  async def thread_update(self, event_data: dict):
    await self.user_event_functions.thread_update(self.user_resources)

  async def thread_delete(self, event_data: dict):
    await self.user_event_functions.thread_delete(self.user_resources)

  async def thread_list_sync(self, event_data: dict):
    await self.user_event_functions.thread_list_sync(self.user_resources)

  async def thread_member_update(self, event_data: dict):
    await self.user_event_functions.thread_member_update(self.user_resources)

  async def thread_members_update(self, event_data: dict):
    await self.user_event_functions.thread_members_update(self.user_resources)

  async def stage_instance_create(self, event_data: dict):
    await self.user_event_functions.stage_instance_create(self.user_resources)

  async def stage_instance_update(self, event_data: dict):
    await self.user_event_functions.stage_instance_update(self.user_resources)

  async def stage_instance_delete(self, event_data: dict):
    await self.user_event_functions.stage_instance_delete(self.user_resources)

  async def guild_member_add(self, event_data: dict):
    await self.user_event_functions.guild_member_add(self.user_resources)

  async def guild_member_update(self, event_data: dict):
    await self.user_event_functions.guild_member_update(self.user_resources)

  async def guild_members_chunk(self, event_data: dict):
    await self.user_event_functions.guild_members_chunk(self.user_resources)

  async def guild_member_remove(self, event_data: dict):
    await self.user_event_functions.guild_member_remove(self.user_resources)

  async def guild_audit_log_entry_create(self, event_data: dict):
    await self.user_event_functions.guild_audit_log_entry_create(self.user_resources)

  async def guild_ban_add(self, event_data: dict):
    await self.user_event_functions.guild_ban_add(self.user_resources)

  async def guild_ban_remove(self, event_data: dict):
    await self.user_event_functions.guild_ban_remove(self.user_resources)

  async def guild_emojis_update(self, event_data: dict):
    await self.user_event_functions.guild_emojis_update(self.user_resources)

  async def guild_stickers_update(self, event_data: dict):
    await self.user_event_functions.guild_stickers_update(self.user_resources)

  async def guild_soundboard_sound_create(self, event_data: dict):
    await self.user_event_functions.guild_soundboard_sound_create(self.user_resources)

  async def guild_soundboard_sound_update(self, event_data: dict):
    await self.user_event_functions.guild_soundboard_sound_update(self.user_resources)

  async def guild_soundboard_sound_delete(self, event_data: dict):
    await self.user_event_functions.guild_soundboard_sound_delete(self.user_resources)

  async def guild_soundboard_sounds_update(self, event_data: dict):
    await self.user_event_functions.guild_soundboard_sounds_update(self.user_resources)

  async def guild_integrations_update(self, event_data: dict):
    await self.user_event_functions.guild_integrations_update(self.user_resources)

  async def integration_create(self, event_data: dict):
    await self.user_event_functions.integration_create(self.user_resources)

  async def integration_update(self, event_data: dict):
    await self.user_event_functions.integration_update(self.user_resources)

  async def integration_delete(self, event_data: dict):
    await self.user_event_functions.integration_delete(self.user_resources)

  async def interaction_create(self, event_data: dict):
    await self.user_event_functions.interaction_create(self.user_resources)

  async def webhooks_update(self, event_data: dict):
    await self.user_event_functions.webhooks_update(self.user_resources)

  async def invite_create(self, event_data: dict):
    await self.user_event_functions.invite_create(self.user_resources)

  async def invite_delete(self, event_data: dict):
    await self.user_event_functions.invite_delete(self.user_resources)

  async def voice_channel_effect_send(self, event_data: dict):
    await self.user_event_functions.voice_channel_effect_send(self.user_resources)

  async def voice_state_update(self, event_data: dict):
    await self.user_event_functions.voice_state_update(self.user_resources)

  async def presence_update(self, event_data: dict):
    await self.user_event_functions.presence_update(self.user_resources)

  async def message_create(self, event_data: dict):
    await self.user_event_functions.message_create(self.user_resources)

  async def message_update(self, event_data: dict):
    await self.user_event_functions.message_update(self.user_resources)

  async def message_delete(self, event_data: dict):
    await self.user_event_functions.message_delete(self.user_resources)

  async def message_delete_bulk(self, event_data: dict):
    await self.user_event_functions.message_delete_bulk(self.user_resources)

  async def message_reaction_add(self, event_data: dict):
    await self.user_event_functions.message_reaction_add(self.user_resources)

  async def message_reaction_remove(self, event_data: dict):
    await self.user_event_functions.message_reaction_remove(self.user_resources)

  async def message_reaction_remove_all(self, event_data: dict):
    await self.user_event_functions.message_reaction_remove_all(self.user_resources)

  async def message_reaction_remove_emoji(self, event_data: dict):
    await self.user_event_functions.message_reaction_remove_emoji(self.user_resources)

  async def typing_start(self, event_data: dict):
    await self.user_event_functions.typing_start(self.user_resources)

  async def user_update(self, event_data: dict):
    await self.user_event_functions.user_update(self.user_resources)

  async def guild_scheduled_event_create(self, event_data: dict):
    await self.user_event_functions.guild_scheduled_event_create(self.user_resources)

  async def guild_scheduled_event_update(self, event_data: dict):
    await self.user_event_functions.guild_scheduled_event_update(self.user_resources)

  async def guild_scheduled_event_delete(self, event_data: dict):
    await self.user_event_functions.guild_scheduled_event_delete(self.user_resources)

  async def guild_scheduled_event_user_add(self, event_data: dict):
    await self.user_event_functions.guild_scheduled_event_user_add(self.user_resources)

  async def guild_scheduled_event_user_remove(self, event_data: dict):
    await self.user_event_functions.guild_scheduled_event_user_remove(self.user_resources)

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