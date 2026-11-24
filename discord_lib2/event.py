from discord_lib2.objects.resources import UserEventResources
from discord_lib2.objects.gateway import recv_event_object

snowflake = str

class GatewayEvent:
  async def ready(self, resources: UserEventResources, ready_object: recv_event_object.Ready):
    pass
    
  async def resumed(self, resources: UserEventResources):
    pass

  # auto moderation
  async def auto_moderation_rule_create(self, resources: UserEventResources, auto_moderation_rule_object: recv_event_object.AutoModerationRule):
    pass

  async def auto_moderation_rule_update(self, resources: UserEventResources, auto_moderation_rule_object: recv_event_object.AutoModerationRule):
    pass

  async def auto_moderation_rule_delete(self, resources: UserEventResources, auto_moderation_rule_object: recv_event_object.AutoModerationRule):
    pass

  async def auto_moderation_action_execution(self, resources: UserEventResources, auto_moderation_action_execution_object: recv_event_object.AutoModerationActionExecution):
    pass

  # channel
  async def channel_create(self, resources: UserEventResources, channel_object: recv_event_object.Channel):
    pass

  async def channel_update(self, resources: UserEventResources, channel_object: recv_event_object.Channel):
    pass

  async def channel_delete(self, resources: UserEventResources, channel_object: recv_event_object.Channel):
    pass

  async def channel_info(self, resources: UserEventResources, channel_info_object: recv_event_object.ChannelInfo):
    pass

  async def voice_channel_status_update(self, resources: UserEventResources, voice_channel_status_update_object: recv_event_object.VoiceChannelStatusUpdate):
    pass

  async def voice_channel_start_time_update(self, resources: UserEventResources, voice_channel_start_time_update_object: recv_event_object.VoiceChannelStartTimeUpdate):
    pass

  async def thread_create(self, resources: UserEventResources, channel_object: recv_event_object.Channel, new: bool):
    pass

  async def thread_update(self, resources: UserEventResources, channel_object: recv_event_object.Channel):
    pass

  async def thread_delete(self, resources: UserEventResources, channel_object: recv_event_object.Channel):
    pass

  async def thread_list_sync(self, resources: UserEventResources, thread_list_sync_object: recv_event_object.ThreadListSync):
    pass

  async def thread_member_update(self, resources: UserEventResources, thread_member_object: recv_event_object.Channel.ThreadMember):
    pass

  async def thread_members_update(self, resources: UserEventResources, thread_member_object: recv_event_object.ThreadMembersUpdate):
    pass

  async def channel_pins_update(self, resources: UserEventResources, channel_pins_update_object: recv_event_object.ChannelPinsUpdate):
    pass

  # entitlement
  async def entitlement_create(self, resources: UserEventResources, entitlement_object: recv_event_object.Entitlement):
    pass

  async def entitlement_update(self, resources: UserEventResources, entitlement_object: recv_event_object.Entitlement):
    pass

  async def entitlement_delete(self, resources: UserEventResources, entitlement_object: recv_event_object.Entitlement):
    pass

  # guilds
  async def guild_create(self, resources: UserEventResources, guild_create_object: recv_event_object.GuildCreate):
    pass

  async def guild_update(self, resources: UserEventResources, guild_object: recv_event_object.Guild):
    pass

  async def guild_delete(self, resources: UserEventResources, guild_object: recv_event_object.Guild):
    pass

  async def guild_audit_log_entry_create(self, resources: UserEventResources):
    pass

  async def guild_ban_add(self, resources: UserEventResources, guild_ban_add_object: recv_event_object.GuildBanEvent):
    pass

  async def guild_ban_remove(self, resources: UserEventResources, guild_ban_remove_object: recv_event_object.GuildBanEvent):
    pass

  async def guild_emojis_update(self, resources: UserEventResources, guild_emojis_update_object: recv_event_object.GuildEmojisUpdate):
    pass

  async def guild_stickers_update(self, resources: UserEventResources, guild_stickers_update_object: recv_event_object.GuildStickersUpdate):
    pass

  async def guild_integrations_update(self, resources: UserEventResources):
    pass

  async def guild_member_add(self, resources: UserEventResources, guild_member_add_object: recv_event_object.GuildMemberAdd, new: bool):
    pass

  async def guild_member_remove(self, resources: UserEventResources, guild_member_remove_object: recv_event_object.GuildMemberRemove):
    pass

  async def guild_member_update(self, resources: UserEventResources, guild_member_update_object: recv_event_object.GuildMemberUpdate):
    pass

  async def guild_members_chunk(self, resources: UserEventResources, guild_members_chunk_object: recv_event_object.GuildMembersChunk):
    pass

  async def guild_role_create(self, resources: UserEventResources, guild_role_object: recv_event_object.GuildRoleEvent):
    pass

  async def guild_role_update(self, resources: UserEventResources, guild_role_object: recv_event_object.GuildRoleEvent):
    pass

  async def guild_role_delete(self, resources: UserEventResources, guild_role_delete_object: recv_event_object.GuildRoleDelete):
    pass

  async def guild_scheduled_event_create(self, resources: UserEventResources, guild_scheduled_event_object: recv_event_object.GuildScheduledEvent):
    pass

  async def guild_scheduled_event_update(self, resources: UserEventResources, guild_scheduled_event_object: recv_event_object.GuildScheduledEvent):
    pass

  async def guild_scheduled_event_delete(self, resources: UserEventResources, guild_scheduled_event_object: recv_event_object.GuildScheduledEvent):
    pass

  async def guild_scheduled_event_user_add(self, resources: UserEventResources, guild_scheduled_event_user_add_object: recv_event_object.GuildScheduledEventUserAdd):
    pass

  async def guild_scheduled_event_user_remove(self, resources: UserEventResources, guild_scheduled_event_user_remove_object: recv_event_object.GuildScheduledEventUserRemove):
    pass

  async def guild_soundboard_sound_create(self, resources: UserEventResources, soundboard_sound_object: recv_event_object.SoundboardSound):
    pass

  async def guild_soundboard_sound_update(self, resources: UserEventResources, soundboard_sound_object: recv_event_object.SoundboardSound):
    pass

  async def guild_soundboard_sound_delete(self, resources: UserEventResources, soundboard_sound_delete_object: recv_event_object.GuildSoundboardSoundDelete):
    pass

  async def guild_soundboard_sounds_update(self, resources: UserEventResources, soundboard_sounds_update_object: recv_event_object.GuildSoundboardSoundsUpdate):
    pass

  async def soundboard_sounds(self, resources: UserEventResources, soundboard_sounds_object: recv_event_object.GuildSoundboardSoundsUpdate):
    pass

  # integration
  async def integration_create(self, resources: UserEventResources, integration_object: recv_event_object.IntegrationEvent):
    pass

  async def integration_update(self, resources: UserEventResources, integration_object: recv_event_object.IntegrationEvent):
    pass

  async def integration_delete(self, resources: UserEventResources, integration_delete_object: recv_event_object.IntegrationDelete):
    pass

  # invite
  async def invite_create(self, resources: UserEventResources, invite_object: recv_event_object.InviteCreate):
    pass

  async def invite_delete(self, resources: UserEventResources, invite_delete_object: recv_event_object.InviteDelete):
    pass

  # message
  async def message_create(self, resources: UserEventResources, message_create_object: recv_event_object.MessageCreateUpdate):
    pass

  async def message_update(self, resources: UserEventResources, message_update_object: recv_event_object.MessageCreateUpdate):
    pass

  async def message_delete(self, resources: UserEventResources, message_delete_object: recv_event_object.MessageDelete):
    pass

  async def message_delete_bulk(self, resources: UserEventResources, message_delete_bulk_object: recv_event_object.MessageDeleteBulk):
    pass

  async def message_reaction_add(self, resources: UserEventResources, message_reaction_add_objct: recv_event_object.MessageReactionAdd):
    pass

  async def message_reaction_remove(self, resources: UserEventResources, message_reaction_remove_object: recv_event_object.MessageReactionRemove):
    pass

  async def message_reaction_remove_all(self, resources: UserEventResources, message_reaction_remove_all_object: recv_event_object.MessageReactionRemoveAll):
    pass

  async def message_reaction_remove_emoji(self, resources: UserEventResources, mrre_object: recv_event_object.MessageReactionRemoveEmoji):
    pass

  # presence
  async def presence_update(self, resources: UserEventResources, presence_update_object: recv_event_object.PresenceUpdate):
    pass

  async def typing_start(self, resources: UserEventResources, typing_start_object: recv_event_object.TypingStart):
    pass

  async def user_update(self, resources: UserEventResources, user_object: recv_event_object.User):
    pass

  # voice
  async def voice_channel_effect_send(self, resources: UserEventResources, voice_channel_effect_send_object: recv_event_object.VoiceChannelEffectSend):
    pass

  async def voice_state_update(self, resources: UserEventResources, voice_state_object: recv_event_object.VoiceState):
    pass

  async def voice_server_update(self, resources: UserEventResources, voice_server_update_object: recv_event_object.VoiceServerUpdate):
    pass

  # webhook
  async def webhooks_update(self, resources: UserEventResources, webhooks_update_object: recv_event_object.WebhooksUpdate):
    pass

  # interaction
  async def interaction_create(self, resources: UserEventResources, interaction_object: recv_event_object.PingInteraction | recv_event_object.ApplicationCommandAutocompleteInteraction | recv_event_object.ApplicationCommandInteraction | recv_event_object.MessageComponentInteraction | recv_event_object.ModulSubmitInteraction):
    pass

  # stage instance
  async def stage_instance_create(self, resources: UserEventResources, stage_instance_object: recv_event_object.StageInstance):
    pass

  async def stage_instance_update(self, resources: UserEventResources, stage_instance_object: recv_event_object.StageInstance):
    pass

  async def stage_instance_delete(self, resources: UserEventResources, stage_instance_object: recv_event_object.StageInstance):
    pass

  # poll
  async def message_poll_vote_add(self, resources: UserEventResources, message_poll_vote_object: recv_event_object.MessagePollVote):
    pass

  async def message_poll_vote_remove(self, resources: UserEventResources, message_poll_vote_object: recv_event_object.MessagePollVote):
    pass

  # __library event
  async def gateway_close_event(self, resources: UserEventResources):
    pass