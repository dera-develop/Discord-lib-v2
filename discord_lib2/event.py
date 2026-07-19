from discord_lib2.objects.resources import UserEventResources

class GatewayEvent:
  def __init__(self) -> None:
    pass

  async def ready(self, resources: UserEventResources):
    pass

  async def resumed(self, resources: UserEventResources):
    pass

  async def guild_create(self, resources: UserEventResources):
    pass

  async def guild_update(self, resources: UserEventResources):
    pass

  async def guild_delete(self, resources: UserEventResources):
    pass

  async def guild_role_create(self, resources: UserEventResources):
    pass

  async def guild_role_update(self, resources: UserEventResources):
    pass

  async def guild_role_delete(self, resources: UserEventResources):
    pass

  async def channel_create(self, resources: UserEventResources):
    pass

  async def channel_update(self, resources: UserEventResources):
    pass

  async def channel_delete(self, resources: UserEventResources):
    pass

  async def channel_pins_update(self, resources: UserEventResources):
    pass

  async def thread_create(self, resources: UserEventResources):
    pass

  async def thread_update(self, resources: UserEventResources):
    pass

  async def thread_delete(self, resources: UserEventResources):
    pass

  async def thread_list_sync(self, resources: UserEventResources):
    pass

  async def thread_member_update(self, resources: UserEventResources):
    pass

  async def thread_members_update(self, resources: UserEventResources):
    pass

  async def stage_instance_create(self, resources: UserEventResources):
    pass

  async def stage_instance_update(self, resources: UserEventResources):
    pass

  async def stage_instance_delete(self, resources: UserEventResources):
    pass

  async def guild_member_add(self, resources: UserEventResources):
    pass

  async def guild_member_update(self, resources: UserEventResources):
    pass

  async def guild_members_chunk(self, resources: UserEventResources):
    pass

  async def guild_member_remove(self, resources: UserEventResources):
    pass

  async def guild_audit_log_entry_create(self, resources: UserEventResources):
    pass

  async def guild_ban_add(self, resources: UserEventResources):
    pass

  async def guild_ban_remove(self, resources: UserEventResources):
    pass

  async def guild_emojis_update(self, resources: UserEventResources):
    pass

  async def guild_stickers_update(self, resources: UserEventResources):
    pass

  async def guild_soundboard_sound_create(self, resources: UserEventResources):
    pass

  async def guild_soundboard_sound_update(self, resources: UserEventResources):
    pass

  async def guild_soundboard_sound_delete(self, resources: UserEventResources):
    pass

  async def guild_soundboard_sounds_update(self, resources: UserEventResources):
    pass

  async def guild_integrations_update(self, resources: UserEventResources):
    pass

  async def integration_create(self, resources: UserEventResources):
    pass

  async def integration_update(self, resources: UserEventResources):
    pass

  async def integration_delete(self, resources: UserEventResources):
    pass

  async def interaction_create(self, resources: UserEventResources):
    pass

  async def webhooks_update(self, resources: UserEventResources):
    pass

  async def invite_create(self, resources: UserEventResources):
    pass

  async def invite_delete(self, resources: UserEventResources):
    pass

  async def voice_channel_effect_send(self, resources: UserEventResources):
    pass

  async def voice_state_update(self, resources: UserEventResources):
    pass

  async def presence_update(self, resources: UserEventResources):
    pass

  async def message_create(self, resources: UserEventResources):
    pass

  async def message_update(self, resources: UserEventResources):
    pass

  async def message_delete(self, resources: UserEventResources):
    pass

  async def message_delete_bulk(self, resources: UserEventResources):
    pass

  async def message_reaction_add(self, resources: UserEventResources):
    pass

  async def message_reaction_remove(self, resources: UserEventResources):
    pass

  async def message_reaction_remove_all(self, resources: UserEventResources):
    pass

  async def message_reaction_remove_emoji(self, resources: UserEventResources):
    pass

  async def typing_start(self, resources: UserEventResources):
    pass

  async def user_update(self, resources: UserEventResources):
    pass

  async def guild_scheduled_event_create(self, resources: UserEventResources):
    pass

  async def guild_scheduled_event_update(self, resources: UserEventResources):
    pass

  async def guild_scheduled_event_delete(self, resources: UserEventResources):
    pass

  async def guild_scheduled_event_user_add(self, resources: UserEventResources):
    pass

  async def guild_scheduled_event_user_remove(self, resources: UserEventResources):
    pass

  async def auto_moderation_rule_create(self, resources: UserEventResources):
    pass

  async def auto_moderation_rule_update(self, resources: UserEventResources):
    pass

  async def auto_moderation_rule_delete(self, resources: UserEventResources):
    pass

  async def auto_moderation_action_execution(self, resources: UserEventResources):
    pass

  async def message_poll_vote_add(self, resources: UserEventResources):
    pass

  async def message_poll_vote_remove(self, resources: UserEventResources):
    pass