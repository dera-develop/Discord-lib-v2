import dacite
from typing import Any, TypeVar
from logging import Logger

from discord_lib2.event import GatewayEvent
from discord_lib2.objects.resources import UserEventResources
from discord_lib2.objects.gateway import recv_event_object

T = TypeVar("T")

class UserEventTrigger:
  def __init__(self, logger: Logger, resources: UserEventResources, user_event: GatewayEvent) -> None:
    self.logger = logger
    self.resources = resources
    self.user_event = user_event

  def load_object(self, target_class: type[T], source_data: dict[str, Any]) -> T|None:
    try:
      return dacite.from_dict(target_class, source_data)
    except dacite.DaciteError as e:
      self.logger.error(f"receive data parse error | {str(e)}")

  async def ready(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Ready, event_data)
    if obj is None: return
    await self.user_event.ready(self.resources, obj)
    
  async def resumed(self, event_data: dict[str, Any]):
    await self.user_event.resumed(self.resources)

  # auto moderation
  async def auto_moderation_rule_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.AutoModerationRule, event_data)
    if obj is None: return
    await self.user_event.auto_moderation_rule_create(self.resources, obj)

  async def auto_moderation_rule_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.AutoModerationRule, event_data)
    if obj is None: return
    await self.user_event.auto_moderation_rule_update(self.resources, obj)

  async def auto_moderation_rule_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.AutoModerationRule, event_data)
    if obj is None: return
    await self.user_event.auto_moderation_rule_update(self.resources, obj)

  async def auto_moderation_action_execution(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.AutoModerationActionExecution, event_data)
    if obj is None: return
    await self.user_event.auto_moderation_action_execution(self.resources, obj)

  # channel
  async def channel_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.channel_create(self.resources, obj)

  async def channel_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.channel_update(self.resources, obj)

  async def channel_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.channel_delete(self.resources, obj)

  async def channel_info(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.ChannelInfo, event_data)
    if obj is None: return
    await self.user_event.channel_info(self.resources, obj)

  async def voice_channel_status_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.VoiceChannelStatusUpdate, event_data)
    if obj is None: return
    await self.user_event.voice_channel_status_update(self.resources, obj)

  async def voice_channel_start_time_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.VoiceChannelStartTimeUpdate, event_data)
    if obj is None: return
    await self.user_event.voice_channel_start_time_update(self.resources, obj)

  async def thread_create(self, event_data: dict[str, Any]):
    new: bool = event_data.pop("newly_created", False)
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.thread_create(self.resources, obj, new)

  async def thread_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.thread_update(self.resources, obj)

  async def thread_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel, event_data)
    if obj is None: return
    await self.user_event.thread_delete(self.resources, obj)

  async def thread_list_sync(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.ThreadListSync, event_data)
    if obj is None: return
    await self.user_event.thread_list_sync(self.resources, obj)

  async def thread_member_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Channel.ThreadMember, event_data)
    if obj is None: return
    await self.user_event.thread_member_update(self.resources, obj)

  async def thread_members_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.ThreadMembersUpdate, event_data)
    if obj is None: return
    await self.user_event.thread_members_update(self.resources, obj)

  async def channel_pins_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.ChannelPinsUpdate, event_data)
    if obj is None: return
    await self.user_event.channel_pins_update(self.resources, obj)

  # entitlement
  async def entitlement_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Entitlement, event_data)
    if obj is None: return
    await self.user_event.entitlement_create(self.resources, obj)

  async def entitlement_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Entitlement, event_data)
    if obj is None: return
    await self.user_event.entitlement_update(self.resources, obj)

  async def entitlement_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Entitlement, event_data)
    if obj is None: return
    await self.user_event.entitlement_delete(self.resources, obj)

  # guilds
  async def guild_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildCreate, event_data)
    if obj is None: return
    await self.user_event.guild_create(self.resources, obj)

  async def guild_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Guild, event_data)
    if obj is None: return
    await self.user_event.guild_update(self.resources, obj)

  async def guild_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.Guild, event_data)
    if obj is None: return
    await self.user_event.guild_delete(self.resources, obj)

  async def guild_audit_log_entry_create(self, event_data: dict[str, Any]):
    #TODO
    await self.user_event.guild_audit_log_entry_create(self.resources)

  async def guild_ban_add(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildBanEvent, event_data)
    if obj is None: return
    await self.user_event.guild_ban_add(self.resources, obj)

  async def guild_ban_remove(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildBanEvent, event_data)
    if obj is None: return
    await self.user_event.guild_ban_remove(self.resources, obj)

  async def guild_emojis_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildEmojisUpdate, event_data)
    if obj is None: return
    await self.user_event.guild_emojis_update(self.resources, obj)

  async def guild_stickers_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildStickersUpdate, event_data)
    if obj is None: return
    await self.user_event.guild_stickers_update(self.resources, obj)

  async def guild_integrations_update(self, event_data: dict[str, Any]):
    #TODO
    await self.user_event.guild_integrations_update(self.resources)

  async def guild_member_add(self, event_data: dict[str, Any]):
    new = event_data.pop("__LIB_DATA_NEW", False)
    obj = self.load_object(recv_event_object.GuildMemberAdd, event_data)
    if obj is None: return
    await self.user_event.guild_member_add(self.resources, obj, new)

  async def guild_member_remove(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildMemberRemove, event_data)
    if obj is None: return
    await self.user_event.guild_member_remove(self.resources, obj)

  async def guild_member_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildMemberUpdate, event_data)
    if obj is None: return
    await self.user_event.guild_member_update(self.resources, obj)

  async def guild_members_chunk(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildMembersChunk, event_data)
    if obj is None: return
    await self.user_event.guild_members_chunk(self.resources, obj)

  async def guild_role_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildRoleEvent, event_data)
    if obj is None: return
    await self.user_event.guild_role_create(self.resources, obj)

  async def guild_role_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildRoleEvent, event_data)
    if obj is None: return
    await self.user_event.guild_role_update(self.resources, obj)

  async def guild_role_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildRoleDelete, event_data)
    if obj is None: return
    await self.user_event.guild_role_delete(self.resources, obj)

  async def guild_scheduled_event_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildScheduledEvent, event_data)
    if obj is None: return
    await self.user_event.guild_scheduled_event_create(self.resources, obj)

  async def guild_scheduled_event_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildScheduledEvent, event_data)
    if obj is None: return
    await self.user_event.guild_scheduled_event_update(self.resources, obj)

  async def guild_scheduled_event_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildScheduledEvent, event_data)
    if obj is None: return
    await self.user_event.guild_scheduled_event_delete(self.resources, obj)

  async def guild_scheduled_event_user_add(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildScheduledEventUserAdd, event_data)
    if obj is None: return
    await self.user_event.guild_scheduled_event_user_add(self.resources, obj)

  async def guild_scheduled_event_user_remove(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildScheduledEventUserRemove, event_data)
    if obj is None: return
    await self.user_event.guild_scheduled_event_user_remove(self.resources, obj)

  async def guild_soundboard_sound_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.SoundboardSound, event_data)
    if obj is None: return
    await self.user_event.guild_soundboard_sound_create(self.resources, obj)

  async def guild_soundboard_sound_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.SoundboardSound, event_data)
    if obj is None: return
    await self.user_event.guild_soundboard_sound_update(self.resources, obj)

  async def guild_soundboard_sound_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildSoundboardSoundDelete, event_data)
    if obj is None: return
    await self.user_event.guild_soundboard_sound_delete(self.resources, obj)

  async def guild_soundboard_sounds_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildSoundboardSoundsUpdate, event_data)
    if obj is None: return
    await self.user_event.guild_soundboard_sounds_update(self.resources, obj)

  async def soundboard_sounds(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.GuildSoundboardSoundsUpdate, event_data)
    if obj is None: return
    await self.user_event.soundboard_sounds(self.resources, obj)

  # integration
  async def integration_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.IntegrationEvent, event_data)
    if obj is None: return
    await self.user_event.integration_create(self.resources, obj)

  async def integration_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.IntegrationEvent, event_data)
    if obj is None: return
    await self.user_event.integration_update(self.resources, obj)

  async def integration_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.IntegrationDelete, event_data)
    if obj is None: return
    await self.user_event.integration_delete(self.resources, obj)

  # invite
  async def invite_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.InviteCreate, event_data)
    if obj is None: return
    await self.user_event.invite_create(self.resources, obj)

  async def invite_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.InviteDelete, event_data)
    if obj is None: return
    await self.user_event.invite_delete(self.resources, obj)

  # message
  async def message_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageCreateUpdate, event_data)
    if obj is None: return
    await self.user_event.message_create(self.resources, obj)

  async def message_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageCreateUpdate, event_data)
    if obj is None: return
    await self.user_event.message_update(self.resources, obj)

  async def message_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageDelete, event_data)
    if obj is None: return
    await self.user_event.message_delete(self.resources, obj)

  async def message_delete_bulk(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageDeleteBulk, event_data)
    if obj is None: return
    await self.user_event.message_delete_bulk(self.resources, obj)

  async def message_reaction_add(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageReactionAdd, event_data)
    if obj is None: return
    await self.user_event.message_reaction_add(self.resources, obj)

  async def message_reaction_remove(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageReactionRemove, event_data)
    if obj is None: return
    await self.user_event.message_reaction_remove(self.resources, obj)

  async def message_reaction_remove_all(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageReactionRemoveAll, event_data)
    if obj is None: return
    await self.user_event.message_reaction_remove_all(self.resources, obj)

  async def message_reaction_remove_emoji(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessageReactionRemoveEmoji, event_data)
    if obj is None: return
    await self.user_event.message_reaction_remove_emoji(self.resources, obj)

  # presence
  async def presence_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.PresenceUpdate, event_data)
    if obj is None: return
    await self.user_event.presence_update(self.resources, obj)

  async def typing_start(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.TypingStart, event_data)
    if obj is None: return
    await self.user_event.typing_start(self.resources, obj)

  async def user_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.User, event_data)
    if obj is None: return
    await self.user_event.user_update(self.resources, obj)

  # voice
  async def voice_channel_effect_send(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.VoiceChannelEffectSend, event_data)
    if obj is None: return
    await self.user_event.voice_channel_effect_send(self.resources, obj)

  async def voice_state_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.VoiceState, event_data)
    if obj is None: return
    await self.user_event.voice_state_update(self.resources, obj)

  async def voice_server_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.VoiceServerUpdate, event_data)
    if obj is None: return
    await self.user_event.voice_server_update(self.resources, obj)

  # webhook
  async def webhooks_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.WebhooksUpdate, event_data)
    if obj is None: return
    await self.user_event.webhooks_update(self.resources, obj)

  # interaction
  async def interaction_create(self, event_data: dict[str, Any]):
    IT_PING = 1
    IT_APPLICATION_COMMNAND = 2
    IT_MESSAGE_COMPONENT = 3
    IT_APPLICATION_COMMAND_AUTOCOMPLETE = 4
    IT_MODUL_SUBMIT = 5
    interaction_type: int = event_data["type"]
    if interaction_type == IT_PING:
      obj = self.load_object(recv_event_object.PingInteraction, event_data)
    elif interaction_type == IT_APPLICATION_COMMNAND:
      obj = self.load_object(recv_event_object.ApplicationCommandInteraction, event_data)
    elif interaction_type == IT_MESSAGE_COMPONENT:
      obj = self.load_object(recv_event_object.MessageComponentInteraction, event_data)
    elif interaction_type == IT_APPLICATION_COMMAND_AUTOCOMPLETE:
      obj = self.load_object(recv_event_object.ApplicationCommandAutocompleteInteraction, event_data)
    elif interaction_type == IT_MODUL_SUBMIT:
      obj = self.load_object(recv_event_object.ModulSubmitInteraction, event_data)
    else:
      self.logger.error("invalid interaction type")
      obj = None
    if obj is None: return
    await self.user_event.interaction_create(self.resources, obj)

  # stage instance
  async def stage_instance_create(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.StageInstance, event_data)
    if obj is None: return
    await self.user_event.stage_instance_create(self.resources, obj)

  async def stage_instance_update(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.StageInstance, event_data)
    if obj is None: return
    await self.user_event.stage_instance_update(self.resources, obj)

  async def stage_instance_delete(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.StageInstance, event_data)
    if obj is None: return
    await self.user_event.stage_instance_delete(self.resources, obj)

  # poll
  async def message_poll_vote_add(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessagePollVote, event_data)
    if obj is None: return
    await self.user_event.message_poll_vote_add(self.resources, obj)

  async def message_poll_vote_remove(self, event_data: dict[str, Any]):
    obj = self.load_object(recv_event_object.MessagePollVote, event_data)
    if obj is None: return
    await self.user_event.message_poll_vote_remove(self.resources, obj)

  # __library event
  async def gateway_close_event(self, event_data: dict[str, Any]):
    pass