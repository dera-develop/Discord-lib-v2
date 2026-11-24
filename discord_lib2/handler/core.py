from logging import Logger

from discord_lib2.logger import Logger as MLogger

from discord_lib2.handler.dispatcher import EventDispatcher
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.network.http_request.http import HttpRequestController
from discord_lib2.network.http_request.request_loader import RequestLoader
from discord_lib2.network.gateway.websocket import WebsocketController

# cache update
from discord_lib2.handler.cache_update.base_class import HTTPcontroller
from discord_lib2.handler.cache_update.connection import CacheConnection
from discord_lib2.handler.cache_update.auto_moderation import CacheAutoModeration
from discord_lib2.handler.cache_update.channels import CacheChannels
from discord_lib2.handler.cache_update.guild import CacheGuild
from discord_lib2.handler.cache_update.integration import CacheIntegration
from discord_lib2.handler.cache_update.invite import CacheInvite
from discord_lib2.handler.cache_update.message import CacheMessage
from discord_lib2.handler.cache_update.voice import CacheVoice
from discord_lib2.handler.cache_update.webhook import CacheWebhook
from discord_lib2.handler.cache_update.interaction import CacheInteraction
from discord_lib2.handler.cache_update.stage_instance import CacheStageInstance
from discord_lib2.handler.cache_update.subscription import CacheSubscription
from discord_lib2.handler.cache_update.poll import CachePoll

# application command
from discord_lib2.objects.resources import ApplicationCommandResources
from discord_lib2.command.application_command import GuildApplicationCommand, GlobalApplicationCommand
from discord_lib2.handler.tasks.application_command import TaskApplicationCommand

# user event
from discord_lib2.handler.user_event import UserEventTrigger
from discord_lib2.event import GatewayEvent
from discord_lib2.objects.resources import UserEventResources

class EventHandlerCore:
  def __init__(
      self,
      logger: MLogger,
      exception_catcher: ExceptionCatcher2,
      data_cache: DataCacheVault,
      system_cache: SystemCacheVault,
      http_controller: HttpRequestController,
      http_loader: RequestLoader,
      gateway_controller: WebsocketController,
      user_event_resources: UserEventResources,
      appcom_resources: ApplicationCommandResources,
      appcom_datas: dict,
      user_event: GatewayEvent
  ) -> None:
    self.logger = logger
    self.exception_catcher = exception_catcher
    self.data_cache = data_cache
    self.system_cache = system_cache
    self.httpapi = HTTPcontroller(http_controller, http_loader)
    self.gateway_controller = gateway_controller
    self.appcom_resources = appcom_resources
    self.dispatcher = EventDispatcher(logger.get_child("Handler.Dispatcher"), exception_catcher, gateway_controller)
    self.global_appcoms: dict[str, GlobalApplicationCommand] = appcom_datas["globals"]
    self.guild_appcoms: dict[str, dict[str, GuildApplicationCommand]] = appcom_datas["guilds"]

    self.user_event_trigger = UserEventTrigger(self.logger.get_child("User-Event"), user_event_resources, user_event)
    self.__regist_functions()

  def __gen_child_logger(self, child_name: str) -> Logger:
    return self.logger.get_child(f"Handler.{child_name}")

  def __regist_cache_functions(self):
    cache_updator_logger = self.__gen_child_logger("Cache")
    # cache_update/connection
    self.dispatcher.regist_cache_functions(CacheConnection(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi, self.system_cache, self.gateway_controller).get_functions())
    # cache_update/auto_moderation
    self.dispatcher.regist_cache_functions(CacheAutoModeration(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/channels
    self.dispatcher.regist_cache_functions(CacheChannels(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi, self.system_cache).get_functions())
    # cache_update/guild
    self.dispatcher.regist_cache_functions(CacheGuild(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi, self.system_cache, self.gateway_controller).get_functions())
    # cache_update/integration
    self.dispatcher.regist_cache_functions(CacheIntegration(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/invite
    self.dispatcher.regist_cache_functions(CacheInvite(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi, self.system_cache).get_functions())
    # cache_update/message
    self.dispatcher.regist_cache_functions(CacheMessage(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/voice
    self.dispatcher.regist_cache_functions(CacheVoice(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi, self.system_cache).get_functions())
    # cache_update/webhook
    self.dispatcher.regist_cache_functions(CacheWebhook(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/interaction
    self.dispatcher.regist_cache_functions(CacheInteraction(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/stage_instance
    self.dispatcher.regist_cache_functions(CacheStageInstance(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/subscription
    self.dispatcher.regist_cache_functions(CacheSubscription(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())
    # cache_update/poll
    self.dispatcher.regist_cache_functions(CachePoll(cache_updator_logger, self.exception_catcher, self.data_cache, self.httpapi).get_functions())

  def __regist_lib_task_functions(self):
    self.dispatcher.regist_lib_task_functions(TaskApplicationCommand(
      self.__gen_child_logger("Task.Appcom"),
      self.exception_catcher,
      self.data_cache,
      self.httpapi,
      self.system_cache,
      self.appcom_resources,
      self.guild_appcoms,
      self.global_appcoms
    ).get_functions())

  def __regist_user_event_functions(self):
    self.dispatcher.regist_user_event_functions({
      "READY": self.user_event_trigger.ready,
      "RESUMED": self.user_event_trigger.resumed,
      "AUTO_MODERATION_RULE_CREATE": self.user_event_trigger.auto_moderation_rule_create,
      "AUTO_MODERATION_RULE_UPDATE": self.user_event_trigger.auto_moderation_rule_update,
      "AUTO_MODERATION_RULE_DELETE": self.user_event_trigger.auto_moderation_rule_delete,
      "AUTO_MODERATION_ACTION_EXECUTION": self.user_event_trigger.auto_moderation_action_execution,
      "CHANNEL_CREATE": self.user_event_trigger.channel_create,
      "CHANNEL_UPDATE": self.user_event_trigger.channel_update,
      "CHANNEL_DELETE": self.user_event_trigger.channel_delete,
      "CHANNEL_INFO": self.user_event_trigger.channel_info,
      "VOICE_CHANNEL_STATUS_UPDATE": self.user_event_trigger.voice_channel_status_update,
      "VOICE_CHANNEL_START_TIME_UPDATE": self.user_event_trigger.voice_channel_start_time_update,
      "THREAD_CREATE": self.user_event_trigger.thread_create,
      "THREAD_UPDATE": self.user_event_trigger.thread_update,
      "THREAD_DELETE": self.user_event_trigger.thread_delete,
      "THREAD_LIST_SYNC": self.user_event_trigger.thread_list_sync,
      "THREAD_MEMBER_UPDATE": self.user_event_trigger.thread_member_update,
      "THREAD_MEMBERS_UPDATE": self.user_event_trigger.thread_members_update,
      "CHANNEL_PINS_UPDATE": self.user_event_trigger.channel_pins_update,
      "ENTITLEMENT_CREATE": self.user_event_trigger.entitlement_create,
      "ENTITLEMENT_UPDATE": self.user_event_trigger.entitlement_update,
      "ENTITLEMENT_DELETE": self.user_event_trigger.entitlement_delete,
      "GUILD_CREATE": self.user_event_trigger.guild_create,
      "GUILD_UPDATE": self.user_event_trigger.guild_update,
      "GUILD_DELETE": self.user_event_trigger.guild_delete,
      "GUILD_AUDIT_LOG_ENTRY_CREATE": self.user_event_trigger.guild_audit_log_entry_create,
      "GUILD_BAN_ADD": self.user_event_trigger.guild_ban_add,
      "GUILD_BAN_REMOVE": self.user_event_trigger.guild_ban_remove,
      "GUILD_EMOJIS_UPDATE": self.user_event_trigger.guild_emojis_update,
      "GUILD_STICKERS_UPDATE": self.user_event_trigger.guild_stickers_update,
      "GUILD_INTEGRATIONS_UPDATE": self.user_event_trigger.guild_integrations_update,
      "GUILD_MEMBER_ADD": self.user_event_trigger.guild_member_add,
      "GUILD_MEMBER_REMOVE": self.user_event_trigger.guild_member_remove,
      "GUILD_MEMBER_UPDATE": self.user_event_trigger.guild_member_update,
      "GUILD_MEMBERS_CHUNK": self.user_event_trigger.guild_members_chunk,
      "GUILD_ROLE_CREATE": self.user_event_trigger.guild_role_create,
      "GUILD_ROLE_UPDATE": self.user_event_trigger.guild_role_update,
      "GUILD_ROLE_DELETE": self.user_event_trigger.guild_role_delete,
      "GUILD_SCHEDULED_EVENT_CREATE": self.user_event_trigger.guild_scheduled_event_create,
      "GUILD_SCHEDULED_EVENT_UPDATE": self.user_event_trigger.guild_scheduled_event_update,
      "GUILD_SCHEDULED_EVENT_DELETE": self.user_event_trigger.guild_scheduled_event_delete,
      "GUILD_SCHEDULED_EVENT_USER_ADD": self.user_event_trigger.guild_scheduled_event_user_add,
      "GUILD_SCHEDULED_EVENT_USER_REMOVE": self.user_event_trigger.guild_scheduled_event_user_remove,
      "GUILD_SOUNDBOARD_SOUND_CREATE": self.user_event_trigger.guild_soundboard_sound_create,
      "GUILD_SOUNDBOARD_SOUND_UPDATE": self.user_event_trigger.guild_soundboard_sound_update,
      "GUILD_SOUNDBOARD_SOUND_DELETE": self.user_event_trigger.guild_soundboard_sound_delete,
      "GUILD_SOUNDBOARD_SOUNDS_UPDATE": self.user_event_trigger.guild_soundboard_sounds_update,
      "SOUNDBOARD_SOUNDS": self.user_event_trigger.soundboard_sounds,
      "INTEGRATION_CREATE": self.user_event_trigger.integration_create,
      "INTEGRATION_UPDATE": self.user_event_trigger.integration_update,
      "INTEGRATION_DELETE": self.user_event_trigger.integration_delete,
      "INVITE_CREATE": self.user_event_trigger.invite_create,
      "INVITE_DELETE": self.user_event_trigger.invite_delete,
      "MESSAGE_CREATE": self.user_event_trigger.message_create,
      "MESSAGE_UPDATE": self.user_event_trigger.message_update,
      "MESSAGE_DELETE": self.user_event_trigger.message_delete,
      "MESSAGE_DELETE_BULK": self.user_event_trigger.message_delete_bulk,
      "MESSAGE_REACTION_ADD": self.user_event_trigger.message_reaction_add,
      "MESSAGE_REACTION_REMOVE": self.user_event_trigger.message_reaction_remove,
      "MESSAGE_REACTION_REMOVE_ALL": self.user_event_trigger.message_reaction_remove_all,
      "MESSAGE_REACTION_REMOVE_EMOJI": self.user_event_trigger.message_reaction_remove_emoji,
      "PRESENCE_UPDATE": self.user_event_trigger.presence_update,
      "TYPING_START": self.user_event_trigger.typing_start,
      "USER_UPDATE": self.user_event_trigger.user_update,
      "VOICE_CHANNEL_EFFECT_SEND": self.user_event_trigger.voice_channel_effect_send,
      "VOICE_STATE_UPDATE": self.user_event_trigger.voice_state_update,
      "VOICE_SERVER_UPDATE": self.user_event_trigger.voice_server_update,
      "WEBHOOKS_UPDATE": self.user_event_trigger.webhooks_update,
      "INTERACTION_CREATE": self.user_event_trigger.interaction_create,
      "STAGE_INSTANCE_CREATE": self.user_event_trigger.stage_instance_create,
      "STAGE_INSTANCE_UPDATE": self.user_event_trigger.stage_instance_update,
      "STAGE_INSTANCE_DELETE": self.user_event_trigger.stage_instance_delete,
      "MESSAGE_POLL_VOTE_ADD": self.user_event_trigger.message_poll_vote_add,
      "MESSAGE_POLL_VOTE_REMOVE": self.user_event_trigger.message_poll_vote_remove,
      "__LIB_CLOSE_WEBSOCKET": self.user_event_trigger.gateway_close_event
    })

  def __regist_functions(self):
    self.__regist_cache_functions()
    self.__regist_lib_task_functions()
    self.__regist_user_event_functions()

  async def start(self):
    await self.dispatcher.start()

  async def stop(self):
    await self.dispatcher.stop()