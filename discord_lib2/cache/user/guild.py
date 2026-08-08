from typing import Literal

from discord_lib2.cache.user import base

snowflake = base.snowflake
ISO8601timestamp = base.ISO8601timestamp

#### ROLE ####
class RoleColor(base.UserCacheBase):
  primary_color: int | None = None
  secondary_color: int | None = None
  tertiary_color: int | None = None
  def update(self, data: dict):
    if "primary_color" in data:
      self.primary_color = data.get("primary_color")

    if "secondary_color" in data:
      self.secondary_color = data.get("secondary_color")

    if "tertiary_color" in data:
      self.tertiary_color = data.get("tertiary_color")

class RoleTags(base.UserCacheBase):
  bot_id: snowflake | None = None
  integration_id: snowflake | None = None
  premium_subscriber: None = None
  subscription_listing_id: snowflake | None = None
  available_for_purchase: None = None
  guild_connections: None = None
  def update(self, data: dict):
    if "bot_id" in data:
      self.bot_id = data.get("bot_id")

    if "integration_id" in data:
      self.integration_id = data.get("integration_id")

    if "premium_subscriber" in data:
      self.premium_subscriber = data.get("premium_subscriber")

    if "subscription_listing_id" in data:
      self.subscription_listing_id = data.get("subscription_listing_id")

    if "available_for_purchase" in data:
      self.available_for_purchase = data.get("available_for_purchase")

    if "guild_connections" in data:
      self.guild_connections = data.get("guild_connections")

class Role(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  color: int | None = None
  colors: RoleColor = RoleColor()
  hoist: bool | None = None
  icon: str | None = None
  unicode_emoji: str | None = None
  position: int | None = None
  permissions: str | None = None
  managed: bool | None = None
  mentionable: bool | None = None
  tags: RoleTags = RoleTags()
  flags: int | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "color" in data:
      self.color = data.get("color")

    if "colors" in data:
      colors = data.get("colors")
      if isinstance(colors, dict):
        self.colors.update(colors)

    if "hoist" in data:
      self.hoist = data.get("hoist")

    if "icon" in data:
      self.icon = data.get("icon")

    if "unicode_emoji" in data:
      self.unicode_emoji = data.get("unicode_emoji")

    if "position" in data:
      self.position = data.get("position")

    if "permissions" in data:
      self.permissions = data.get("permissions")

    if "managed" in data:
      self.managed = data.get("managed")

    if "mentionable" in data:
      self.mentionable = data.get("mentionable")

    if "tags" in data:
      tags = data.get("tags")
      if isinstance(tags, dict):
        self.tags.update(tags)

    if "flags" in data:
      self.flags = data.get("flags")
##############

#### EMOJI ####
class Emoji(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  roles: list[snowflake] = []
  user: snowflake | None = None   # user_id
  require_colons: bool | None = None
  managed: bool | None = None
  animated: bool | None = None
  available: bool | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "roles" in data:
      roles = data.get("roles")
      if isinstance(roles, list):
        self.roles = roles

    if "user" in data:
      user = data.get("user")
      if isinstance(user, dict):
        self.user = user.get("id")

    if "require_colons" in data:
      self.require_colons = data.get("require_colons")

    if "managed" in data:
      self.managed = data.get("managed")

    if "animated" in data:
      self.animated = data.get("animated")

    if "available" in data:
      self.available = data.get("available")
###############

#### WELCOME SCREEN ####
class WelcomeScreenChannel(base.UserCacheBase):
  channel_id: snowflake | None = None
  description: str | None = None
  emoji_id: snowflake | None = None
  emoji_name: str | None = None
  def update(self, data: dict):
    if "channel_id" in data:
      self.channel_id = data.get("channel_id")

    if "description" in data:
      self.description = data.get("description")

    if "emoji_id" in data:
      self.emoji_id = data.get("emoji_id")

    if "emoji_name" in data:
      self.emoji_name = data.get("emoji_name")

class WelcomeScreen(base.UserCacheBase):
  description: str | None = None
  welcome_channels: dict[snowflake, WelcomeScreenChannel] = {} # key = channel_id
  def update(self, data: dict):
    if "description" in data:
      self.description = data.get("description")

    if "welcome_channels" in data:
      welcome_channels_all: list[dict] | None = data.get("welcome_channels")
      if isinstance(welcome_channels_all, list):
        for welcome_channel_dict in welcome_channels_all:
          if not isinstance(welcome_channel_dict, dict):
            continue

          welcome_channel_id = welcome_channel_dict.get("id")
          if not isinstance(welcome_channel_id, snowflake):
            continue

          if not welcome_channel_id in welcome_channel_dict:
            self.welcome_channels[welcome_channel_id] = WelcomeScreenChannel()
          self.welcome_channels[welcome_channel_id].update(welcome_channel_dict)
########################

#### STICKER ####
class Sticker(base.UserCacheBase):
  id: snowflake | None = None
  pack_id: snowflake | None = None
  name: str | None = None
  description: str | None = None
  tags: str | None = None
  type: int | None = None
  format_type: int | None = None
  available: bool | None = None
  guild_id: snowflake | None = None
  user: snowflake | None = None   # user_id
  sort_value: int | None = None
  def update(self, data: dict):
    if "id" in data:                                                                                                                                                                                                       
      self.id = data.get("id")                                                                                                                                                                                             

    if "pack_id" in data:
      self.pack_id = data.get("pack_id")

    if "name" in data:
      self.name = data.get("name")

    if "description" in data:
      self.description = data.get("description")

    if "tags" in data:
      self.tags = data.get("tags")

    if "type" in data:
      self.type = data.get("type")

    if "format_type" in data:
      self.format_type = data.get("format_type")

    if "available" in data:
      self.available = data.get("available")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "user" in data:
      user = data.get("user")
      if isinstance(user, dict):
        self.user = user.get("id")

    if "sort_value" in data:
      self.sort_value = data.get("sort_value")
#################

#### INCIDENTS DATA ####
class IncidentsData(base.UserCacheBase):
  invites_disabled_until: ISO8601timestamp | None = None
  dms_disabled_until: ISO8601timestamp | None = None
  dm_spam_detected_at: ISO8601timestamp | None = None
  raid_detected_at: ISO8601timestamp | None = None
  def update(self, data: dict):
    if "invites_disabled_until" in data:
      self.invites_disabled_until = data.get("invites_disabled_until")

    if "dms_disabled_until" in data:
      self.dms_disabled_until = data.get("dms_disabled_until")

    if "dm_spam_detected_at" in data:
      self.dm_spam_detected_at = data.get("dm_spam_detected_at")

    if "raid_detected_at" in data:
      self.raid_detected_at = data.get("raid_detected_at")
########################

#### VOICE STATE ####
class VoiceState(base.UserCacheBase):
  guild_id: snowflake | None = None
  channel_id: snowflake | None = None
  user_id: snowflake | None = None
  member: snowflake | None = None   # guildmember_id(user_id)
  session_id: str | None = None
  deaf: bool | None = None
  mute: bool | None = None
  self_deaf: bool | None = None
  self_mute: bool | None = None
  self_stream: bool | None = None
  self_video: bool | None = None
  suppress: bool | None = None
  request_to_speak_timestamp: ISO8601timestamp | None = None
  def update(self, data: dict):
    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "channel_id" in data:
      self.channel_id = data.get("channel_id")

    if "user_id" in data:
      self.user_id = data.get("user_id")

    if "member" in data:
      member = data.get("member")
      if isinstance(member, dict):
        user = member.get("user")
        if isinstance(user, dict):
          user_id = user.get("id")
          if isinstance(user_id, snowflake):
            self.member = user_id

    if "session_id" in data:
      self.session_id = data.get("session_id")

    if "deaf" in data:
      self.deaf = data.get("deaf")

    if "mute" in data:
      self.mute = data.get("mute")

    if "self_deaf" in data:
      self.self_deaf = data.get("self_deaf")

    if "self_mute" in data:
      self.self_mute = data.get("self_mute")

    if "self_stream" in data:
      self.self_stream = data.get("self_stream")

    if "self_video" in data:
      self.self_video = data.get("self_video")

    if "suppress" in data:
      self.suppress = data.get("suppress")

    if "request_to_speak_timestamp" in data:
      self.request_to_speak_timestamp = data.get("request_to_speak_timestamp")
#####################

#### GUILD MEMBER ####
class AvatarDecorationData(base.UserCacheBase):
  asset: str | None = None
  sku_id: snowflake | None = None
  def update(self, data: dict):
    if "asset" in data:
      self.asset = data.get("asset")

    if "sku_id" in data:
      self.sku_id = data.get("sku_id")

class Nameplate(base.UserCacheBase):
  sku_id: snowflake | None = None
  asset: str | None = None
  label: str | None = None
  palette: str | None = None
  def update(self, data: dict):
    if "sku_id" in data:
      self.sku_id = data.get("sku_id")

    if "asset" in data:
      self.asset = data.get("asset")

    if "label" in data:
      self.label = data.get("label")

    if "palette" in data:
      self.palette = data.get("palette")

class Collectibles(base.UserCacheBase):
  nameplate: Nameplate = Nameplate()
  def update(self, data: dict):
    if "nameplate" in data:
      nameplate = data.get("nameplate")
      if isinstance(nameplate, dict):
        self.nameplate.update(nameplate)

class GuildMember(base.UserCacheBase):
  user: snowflake | None = None # user_id
  nick: str | None = None
  avatar: str | None = None
  banner: str | None = None
  roles: list[snowflake] = []
  joined_at: ISO8601timestamp | None = None
  premium_since: ISO8601timestamp | None = None
  deaf: bool | None = None
  mute: bool | None = None
  flags: int | None = None
  pending: bool | None = None
  permissions: str | None = None
  communication_disabled_until: ISO8601timestamp | None = None
  avatar_decoration_data: AvatarDecorationData = AvatarDecorationData()
  collectibles: Collectibles = Collectibles()
  voice_state: VoiceState = VoiceState()
  def update(self, data: dict):
    if "user" in data:
      user = data.get("user")
      if isinstance(user, dict):
        self.user = user.get("id")

    if "nick" in data:
      self.nick = data.get("nick")

    if "avatar" in data:
      self.avatar = data.get("avatar")

    if "banner" in data:
      self.banner = data.get("banner")

    if "roles" in data:
      roles = data.get("roles")
      if isinstance(roles, list):
        self.roles = roles

    if "joined_at" in data:
      self.joined_at = data.get("joined_at")

    if "premium_since" in data:
      self.premium_since = data.get("premium_since")

    if "deaf" in data:
      self.deaf = data.get("deaf")

    if "mute" in data:
      self.mute = data.get("mute")

    if "flags" in data:
      self.flags = data.get("flags")

    if "pending" in data:
      self.pending = data.get("pending")

    if "permissions" in data:
      self.permissions = data.get("permissions")

    if "communication_disabled_until" in data:
      self.communication_disabled_until = data.get("communication_disabled_until")

    if "avatar_decoration_data" in data:
      avatar_decoration_data = data.get("avatar_decoration_data")
      if isinstance(avatar_decoration_data, dict):
        self.avatar_decoration_data.update(avatar_decoration_data)

    if "collectibles" in data:
      collectibles = data.get("collectibles")
      if isinstance(collectibles, dict):
        self.collectibles.update(collectibles)
######################

#### CHANNEL ####
class OverWrite(base.UserCacheBase):
  id: snowflake | None = None
  type: int | None = None
  allow: str | None = None
  deny: str | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "type" in data:
      self.type = data.get("type")

    if "allow" in data:
      self.allow = data.get("allow")

    if "deny" in data:
      self.deny = data.get("deny")

class ThreadMetadata(base.UserCacheBase):
  archived: bool | None = None
  auto_archive_duration: int | None = None
  archive_timestamp: ISO8601timestamp | None = None
  locked: bool | None = None
  invitable: bool | None = None
  create_timestamp: ISO8601timestamp | None = None
  def update(self, data: dict):
    if "archived" in data:
      self.archived = data.get("archived")

    if "auto_archive_duration" in data:
      self.auto_archive_duration = data.get("auto_archive_duration")

    if "archive_timestamp" in data:
      self.archive_timestamp = data.get("archive_timestamp")

    if "locked" in data:
      self.locked = data.get("locked")

    if "invitable" in data:
      self.invitable = data.get("invitable")

    if "create_timestamp" in data:
      self.create_timestamp = data.get("create_timestamp")

class ThreadMember(base.UserCacheBase):
  id: snowflake | None = None
  user_id: snowflake | None = None
  join_timestamp: ISO8601timestamp | None = None
  flags: int | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "user_id" in data:
      self.user_id = data.get("user_id")

    if "join_timestamp" in data:
      self.join_timestamp = data.get("join_timestamp")

    if "flags" in data:
      self.flags = data.get("flags")

class ForumTag(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  moderated: bool | None = None
  emoji_id: snowflake | None = None
  emoji_name: str | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "moderated" in data:
      self.moderated = data.get("moderated")

    if "emoji_id" in data:
      self.emoji_id = data.get("emoji_id")

    if "emoji_name" in data:
      self.emoji_name = data.get("emoji_name")

class DefaultReaction(base.UserCacheBase):
  emoji_id: snowflake | None = None
  emoji_name: str | None = None
  def update(self, data: dict):
    if "emoji_id" in data:
      self.emoji_id = data.get("emoji_id")

    if "emoji_name" in data:
      self.emoji_name = data.get("emoji_name")

class Thread(base.UserCacheBase):
  id: snowflake | None = None
  type: int | None = None
  guild_id: snowflake | None = None
  position: int | None = None
  permission_overwrites: list[OverWrite] = []
  name: str | None = None
  topic: str | None = None
  nsfw: bool | None = None
  last_message_id: snowflake | None = None
  bitrate: int | None = None
  user_limit: int | None = None
  rate_limit_per_user: int | None = None
  recipients: list[snowflake] = [] # user_id
  icon: str | None = None
  owner_id: snowflake | None = None
  application_id: snowflake | None = None
  managed: bool | None = None
  parent_id: snowflake | None = None
  last_pin_timestamp: ISO8601timestamp | None = None
  rtc_region: str | None = None
  video_quality_mode: int | None = None
  message_count: int | None = None
  member_count: int | None = None
  thread_metadata: ThreadMetadata = ThreadMetadata()
  member: ThreadMember = ThreadMember()
  members: dict[snowflake, ThreadMember]
  default_auto_archive_duration: int | None = None
  permissions: str | None = None
  app_permissions: str | None = None
  flags: int | None = None
  total_message_sent: int | None = None
  available_tags: dict[snowflake, ForumTag] = {} # key = forum_tag_id
  applied_tags: list[snowflake] = []
  default_reaction_emoji: DefaultReaction = DefaultReaction()
  default_thread_rate_limit_per_user: int | None = None
  default_sort_order: int | None = None
  default_forum_layout: int | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "type" in data:
      self.type = data.get("type")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "position" in data:
      self.position = data.get("position")

    if "permission_overwrites" in data:
      permission_overwrites = data.get("permission_overwrites")
      if isinstance(permission_overwrites, list):
        self.permission_overwrites = permission_overwrites

    if "name" in data:
      self.name = data.get("name")

    if "topic" in data:
      self.topic = data.get("topic")

    if "nsfw" in data:
      self.nsfw = data.get("nsfw")

    if "last_message_id" in data:
      self.last_message_id = data.get("last_message_id")

    if "bitrate" in data:
      self.bitrate = data.get("bitrate")

    if "user_limit" in data:
      self.user_limit = data.get("user_limit")

    if "rate_limit_per_user" in data:
      self.rate_limit_per_user = data.get("rate_limit_per_user")

    if "recipients" in data:
      recipients = data.get("recipients")
      if isinstance(recipients, list):
        for recipient in recipients:
          if not isinstance(recipient, dict):
            continue
          user_id = recipient.get("id")
          if not isinstance(user_id, snowflake):
            continue
          if not user_id in self.recipients:
            self.recipients.append(user_id)

    if "icon" in data:
      self.icon = data.get("icon")

    if "owner_id" in data:
      self.owner_id = data.get("owner_id")

    if "application_id" in data:
      self.application_id = data.get("application_id")

    if "managed" in data:
      self.managed = data.get("managed")

    if "parent_id" in data:
      self.parent_id = data.get("parent_id")

    if "last_pin_timestamp" in data:
      self.last_pin_timestamp = data.get("last_pin_timestamp")

    if "rtc_region" in data:
      self.rtc_region = data.get("rtc_region")

    if "video_quality_mode" in data:
      self.video_quality_mode = data.get("video_quality_mode")

    if "message_count" in data:
      self.message_count = data.get("message_count")

    if "member_count" in data:
      self.member_count = data.get("member_count")

    if "thread_metadata" in data:
      thread_metadata = data.get("thread_metadata")
      if isinstance(thread_metadata, dict):
        self.thread_metadata.update(thread_metadata)

    if "member" in data:
      member = data.get("member")
      if isinstance(member, dict):
        self.member.update(member)

    if "default_auto_archive_duration" in data:
      self.default_auto_archive_duration = data.get("default_auto_archive_duration")

    if "permissions" in data:
      self.permissions = data.get("permissions")

    if "app_permissions" in data:
      self.app_permissions = data.get("app_permissions")

    if "flags" in data:
      self.flags = data.get("flags")

    if "total_message_sent" in data:
      self.total_message_sent = data.get("total_message_sent")

    if "available_tags" in data:
      available_tags_all: list[dict] | None = data.get("available_tags")
      if isinstance(available_tags_all, list):
        for available_tag_dict in available_tags_all:
          if not isinstance(available_tag_dict, dict):
            continue

          available_tag_id = available_tag_dict.get("id")
          if not isinstance(available_tag_id, snowflake):
            continue

          if not available_tag_id in available_tag_dict:
            self.available_tags[available_tag_id] = ForumTag()
          self.available_tags[available_tag_id].update(available_tag_dict)

    if "applied_tags" in data:
      applied_tags = data.get("applied_tags")
      if isinstance(applied_tags, list):
        self.applied_tags = applied_tags

    if "default_reaction_emoji" in data:
      default_reaction_emoji = data.get("default_reaction_emoji")
      if isinstance(default_reaction_emoji, dict):
        self.default_reaction_emoji.update(default_reaction_emoji)

    if "default_thread_rate_limit_per_user" in data:
      self.default_thread_rate_limit_per_user = data.get("default_thread_rate_limit_per_user")

    if "default_sort_order" in data:
      self.default_sort_order = data.get("default_sort_order")

    if "default_forum_layout" in data:
      self.default_forum_layout = data.get("default_forum_layout")

class Channel(Thread):
  threads: list[snowflake] = []
  def update(self, data: dict):
    if "threads" in data:
      threads = data.get("threads")
      if isinstance(threads, list):
        self.threads = threads
    return super().update(data)
#################

#### STAGE INSTANCE ####
class StageInstance(base.UserCacheBase):
  id: snowflake | None = None
  guild_id: snowflake | None = None
  channel_id: snowflake | None = None
  topic: str | None = None
  privacy_level: int | None = None
  discoverable_disabled: bool | None = None
  guild_scheduled_event_id: snowflake | None = None
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "channel_id" in data:
      self.channel_id = data.get("channel_id")

    if "topic" in data:
      self.topic = data.get("topic")

    if "privacy_level" in data:
      self.privacy_level = data.get("privacy_level")

    if "discoverable_disabled" in data:
      self.discoverable_disabled = data.get("discoverable_disabled")

    if "guild_scheduled_event_id" in data:
      self.guild_scheduled_event_id = data.get("guild_scheduled_event_id")
########################

#### GUILD SCHEDULED EVENT ####
class GuildScheduledEventEntityMetadata(base.UserCacheBase):
  location: str | None = None
  def update(self, data: dict):
    if "location" in data:
      self.location = data.get("location")

class GuildScheduledEventRecurrenceRule(base.UserCacheBase):
  start: ISO8601timestamp | None = None
  end: ISO8601timestamp | None = None
  frequency: int | None = None
  interval: int | None = None
  by_weekday: list[int] = []
  by_n_weekday: list[int] = []
  by_month: list[int] = []
  by_month_day: list[int] = []
  by_year_day: list[int] = []
  count: int | None = None
  def update(self, data: dict):
    if "start" in data:
      self.start = data.get("start")

    if "end" in data:
      self.end = data.get("end")

    if "frequency" in data:
      self.frequency = data.get("frequency")

    if "interval" in data:
      self.interval = data.get("interval")

    if "by_weekday" in data:
      by_weekday = data.get("by_weekday")
      if isinstance(by_weekday, list):
        self.by_weekday = by_weekday

    if "by_n_weekday" in data:
      by_n_weekday = data.get("by_n_weekday")
      if isinstance(by_n_weekday, list):
        self.by_n_weekday = by_n_weekday

    if "by_month" in data:
      by_month = data.get("by_month")
      if isinstance(by_month, list):
        self.by_month = by_month

    if "by_month_day" in data:
      by_month_day = data.get("by_month_day")
      if isinstance(by_month_day, list):
        self.by_month_day = by_month_day

    if "by_year_day" in data:
      by_year_day = data.get("by_year_day")
      if isinstance(by_year_day, list):
        self.by_year_day = by_year_day

    if "count" in data:
      self.count = data.get("count")

class GuildScheduledEvent(base.UserCacheBase):
  id: snowflake | None = None
  guild_id: snowflake | None = None
  channel_id: snowflake | None = None
  creator_id: snowflake | None = None
  name: str | None = None
  description: str | None = None
  scheduled_start_time: ISO8601timestamp | None = None
  scheduled_end_time: ISO8601timestamp | None = None
  privacy_level: int | None = None
  status: int | None = None
  entity_type: int | None = None
  entity_id: snowflake | None = None
  entity_metadata: GuildScheduledEventEntityMetadata = GuildScheduledEventEntityMetadata()
  user_count: int | None = None
  users: list[snowflake] = []
  image: str | None = None
  recurrence_rule: GuildScheduledEventRecurrenceRule = GuildScheduledEventRecurrenceRule()
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "channel_id" in data:
      self.channel_id = data.get("channel_id")

    if "creator_id" in data:
      self.creator_id = data.get("creator_id")

    if "name" in data:
      self.name = data.get("name")

    if "description" in data:
      self.description = data.get("description")

    if "scheduled_start_time" in data:
      self.scheduled_start_time = data.get("scheduled_start_time")

    if "scheduled_end_time" in data:
      self.scheduled_end_time = data.get("scheduled_end_time")

    if "privacy_level" in data:
      self.privacy_level = data.get("privacy_level")

    if "status" in data:
      self.status = data.get("status")

    if "entity_type" in data:
      self.entity_type = data.get("entity_type")

    if "entity_id" in data:
      self.entity_id = data.get("entity_id")

    if "entity_metadata" in data:
      entity_metadata = data.get("entity_metadata")
      if isinstance(entity_metadata, dict):
        self.entity_metadata.update(entity_metadata)

    if "creator" in data:
      if data.get("creator_id") is None:
        user = data.get("creator")
        if isinstance(user, dict):
          user_id = user.get("id")
          if isinstance(user_id, snowflake):
            self.creator_id = user_id

    if "user_count" in data:
      self.user_count = data.get("user_count")

    if "image" in data:
      self.image = data.get("image")

    if "recurrence_rule" in data:
      recurrence_rule = data.get("recurrence_rule")
      if isinstance(recurrence_rule, dict):
        self.recurrence_rule.update(recurrence_rule)
###############################

#### SOUNDBOARD SOUND ####
class SoundboardSound(base.UserCacheBase):
  name: str | None = None
  sound_id: snowflake | None = None
  volume: float | None = None
  emoji_id: snowflake | None = None
  emoji_name: str | None = None
  guild_id: snowflake | None = None
  available: bool | None = None
  user: snowflake | None = None # key = user_id
  def update(self, data: dict):
    if "name" in data:
      self.name = data.get("name")

    if "sound_id" in data:
      self.sound_id = data.get("sound_id")

    if "volume" in data:
      self.volume = data.get("volume")

    if "emoji_id" in data:
      self.emoji_id = data.get("emoji_id")

    if "emoji_name" in data:
      self.emoji_name = data.get("emoji_name")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "available" in data:
      self.available = data.get("available")

    if "user" in data:
      user = data.get("user")
      if isinstance(user, dict):
        self.user = user.get("id")
##########################

#### INTEGRATION ####
class IntegrationAccount(base.UserCacheBase):
  id: str | None = None
  name: str | None = None
  def update(self, data: dict):
    if "id" in data:                                                                                                                                                                                      
      self.id = data.get("id")                                                                                                                                                                            
                                                                                                                                                                                                          
    if "name" in data:                                                                                                                                                                                    
      self.name = data.get("name") 

class IntegrationApplication(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  icon: str | None = None
  description: str | None = None
  bot: snowflake  | None = None # bot_user_id
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "icon" in data:
      self.icon = data.get("icon")

    if "description" in data:
      self.description = data.get("description")

    if "bot" in data:
      bot = data.get("bot")
      if isinstance(bot, dict):
        user_id = bot.get("id")
        if isinstance(user_id, snowflake):
          self.bot = user_id

class Integration(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  type: str | None = None
  enabled: bool | None = None
  syncing: bool | None = None
  role_id: snowflake | None = None
  enable_emoticons: bool | None = None
  expire_behavior: int | None = None
  expire_grace_period: int | None = None
  user: snowflake  | None = None  # user_id
  account: IntegrationAccount = IntegrationAccount()
  synced_at: ISO8601timestamp | None = None
  subscriber_count: int | None = None
  revoked: bool | None = None
  application: IntegrationApplication = IntegrationApplication()
  scopes: list[str] = []
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "type" in data:
      self.type = data.get("type")

    if "enabled" in data:
      self.enabled = data.get("enabled")

    if "syncing" in data:
      self.syncing = data.get("syncing")

    if "role_id" in data:
      self.role_id = data.get("role_id")

    if "enable_emoticons" in data:
      self.enable_emoticons = data.get("enable_emoticons")

    if "expire_behavior" in data:
      self.expire_behavior = data.get("expire_behavior")

    if "expire_grace_period" in data:
      self.expire_grace_period = data.get("expire_grace_period")

    if "user" in data:
      user = data.get("user")
      if isinstance(user, dict):
        self.user = user.get("id")

    if "account" in data:
      account = data.get("account")
      if isinstance(account, dict):
        self.account.update(account)

    if "synced_at" in data:
      self.synced_at = data.get("synced_at")

    if "subscriber_count" in data:
      self.subscriber_count = data.get("subscriber_count")

    if "revoked" in data:
      self.revoked = data.get("revoked")

    if "application" in data:
      application = data.get("application")
      if isinstance(application, dict):
        self.application.update(application)

    if "scopes" in data:
      scopes = data.get("scopes")
      if isinstance(scopes, list):
        self.scopes = scopes
#####################

#### INVITE ####
class Invite(base.UserCacheBase):
  channel_id: snowflake | None = None
  code: str | None = None
  created_at: ISO8601timestamp | None = None
  guild_id: snowflake | None = None
  inviter: snowflake | None = None # user_id
  max_age: int | None = None
  max_uses: int | None = None
  target_type: int | None = None
  target_user: snowflake | None = None # user_id
  target_application: snowflake | None = None # application_id
  temporary: bool | None = None
  uses: int | None = None
  expires_at: ISO8601timestamp | None = None
  role_ids: list[snowflake] = []
  def update(self, data: dict):
    if "channel_id" in data:
      self.channel_id = data.get("channel_id")

    if "code" in data:
      self.code = data.get("code")

    if "created_at" in data:
      self.created_at = data.get("created_at")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "inviter" in data:
      inviter = data.get("inviter")
      if isinstance(inviter, dict):
        user_id = inviter.get("id")
        if isinstance(user_id, snowflake):
          self.inviter = user_id

    if "max_age" in data:
      self.max_age = data.get("max_age")

    if "max_uses" in data:
      self.max_uses = data.get("max_uses")

    if "target_type" in data:
      self.target_type = data.get("target_type")

    if "target_user" in data:
      target_user = data.get("target_user")
      if isinstance(target_user, dict):
        user_id = target_user.get("id")
        if isinstance(user_id, snowflake):
          self.target_user = user_id

    if "target_application" in data:
      self.target_application = data.get("target_application")

    if "temporary" in data:
      self.temporary = data.get("temporary")

    if "uses" in data:
      self.uses = data.get("uses")

    if "expires_at" in data:
      self.expires_at = data.get("expires_at")

    if "role_ids" in data:
      role_ids = data.get("role_ids")
      if isinstance(role_ids, list):
        self.role_ids = role_ids
################

#### GUILD CACHE ####
class GuildCache(base.UserCacheBase):
  id: snowflake | None = None
  name: str | None = None
  icon: str | None = None
  icon_hash: str | None = None
  splash: str | None = None
  discovery_splash: str | None = None
  owner: bool | None = None
  owner_id: snowflake | None = None
  permissions: str | None = None
  region: str | None = None
  afk_channel_id: snowflake | None = None
  afk_timeout: int | None = None
  widget_enabled: bool | None = None
  widget_channel_id: snowflake | None = None
  verification_level: int | None = None
  default_message_notifications: int | None = None
  explicit_content_filter: int | None = None
  roles: dict[snowflake, Role] = {}  # key = role_id
  emojis: dict[snowflake, Emoji] = {}  # key = emoji_id
  features: list[str] | None = None
  mfa_level: int | None = None
  application_id: snowflake | None = None
  system_channel_id: snowflake | None = None
  system_channel_flags: int | None = None
  rules_channel_id: snowflake | None = None
  max_presences: int | None = None
  max_members: int | None = None
  vanity_url_code: str | None = None
  description: str | None = None
  banner: str | None = None
  premium_tier: int | None = None
  premium_subscription_count: int | None = None
  preferred_locale: str | None = None
  public_updates_channel_id: snowflake | None = None
  max_video_channel_users: int | None = None
  max_stage_video_channel_users: int | None = None
  approximate_member_count: int | None = None
  approximate_presence_count: int | None = None
  welcome_screen: WelcomeScreen = WelcomeScreen()
  nsfw_level: int | None = None
  stickers: dict[snowflake, Sticker] = {}  # key = sticker_id
  premium_progress_bar_enabled: bool | None = None
  safety_alerts_channel_id: snowflake | None = None
  incidents_data: IncidentsData = IncidentsData()
  joined_at: ISO8601timestamp | None = None
  large: bool | None = None
  unavailable: bool | None = None
  member_count: int | None = None
  members: dict[snowflake, GuildMember] = {} # key = user_id
  channels: dict[snowflake, Channel] = {}  # key = channel_id
  threads: dict[snowflake, Thread] = {}   # key = channel_id
  stage_instances: dict[snowflake, StageInstance] = {} # key = stage_instance_id
  guild_scheduled_events: dict[snowflake, GuildScheduledEvent] = {}  # key = guild_scheduled_event_id
  soundboard_sounds: dict[snowflake, SoundboardSound] = {} # key = sound_id
  banned_users: list[snowflake] = []
  integrations: dict[snowflake, Integration] = {} # key = integration_id
  invites: dict[str, Invite]
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "name" in data:
      self.name = data.get("name")

    if "icon" in data:
      self.icon = data.get("icon")

    if "icon_hash" in data:
      self.icon_hash = data.get("icon_hash")

    if "splash" in data:
      self.splash = data.get("splash")

    if "discovery_splash" in data:
      self.discovery_splash = data.get("discovery_splash")

    if "owner" in data:
      self.owner = data.get("owner")

    if "owner_id" in data:
      self.owner_id = data.get("owner_id")

    if "permissions" in data:
      self.permissions = data.get("permissions")

    if "region" in data:
      self.region = data.get("region")

    if "afk_channel_id" in data:
      self.afk_channel_id = data.get("afk_channel_id")

    if "afk_timeout" in data:
      self.afk_timeout = data.get("afk_timeout")

    if "widget_enabled" in data:
      self.widget_enabled = data.get("widget_enabled")

    if "widget_channel_id" in data:
      self.widget_channel_id = data.get("widget_channel_id")

    if "verification_level" in data:
      self.verification_level = data.get("verification_level")

    if "default_message_notifications" in data:
      self.default_message_notifications = data.get("default_message_notifications")

    if "explicit_content_filter" in data:
      self.explicit_content_filter = data.get("explicit_content_filter")

    if "roles" in data:
      roles_all = data.get("roles")
      if isinstance(roles_all, list):
        for role_dict in roles_all:
          if not isinstance(role_dict, dict):
            continue

          role_id = role_dict.get("id")
          if not isinstance(role_id, snowflake):
            continue

          if not role_id in role_dict:
            self.roles[role_id] = Role()
          self.roles[role_id].update(role_dict)          

    if "emojis" in data:
      emojis_all = data.get("emojis")
      if isinstance(emojis_all, list):
        for emoji_dict in emojis_all:
          if not isinstance(emoji_dict, dict):
            continue

          emoji_id = emoji_dict.get("id")
          if not isinstance(emoji_id, snowflake):
            continue

          if not emoji_id in emoji_dict:
            self.emojis[emoji_id] = Emoji()
          self.emojis[emoji_id].update(emoji_dict)

    if "features" in data:
      self.features = data.get("features")

    if "mfa_level" in data:
      self.mfa_level = data.get("mfa_level")

    if "application_id" in data:
      self.application_id = data.get("application_id")

    if "system_channel_id" in data:
      self.system_channel_id = data.get("system_channel_id")

    if "system_channel_flags" in data:
      self.system_channel_flags = data.get("system_channel_flags")

    if "rules_channel_id" in data:
      self.rules_channel_id = data.get("rules_channel_id")

    if "max_presences" in data:
      self.max_presences = data.get("max_presences")

    if "max_members" in data:
      self.max_members = data.get("max_members")

    if "vanity_url_code" in data:
      self.vanity_url_code = data.get("vanity_url_code")

    if "description" in data:
      self.description = data.get("description")

    if "banner" in data:
      self.banner = data.get("banner")

    if "premium_tier" in data:
      self.premium_tier = data.get("premium_tier")

    if "premium_subscription_count" in data:
      self.premium_subscription_count = data.get("premium_subscription_count")

    if "preferred_locale" in data:
      self.preferred_locale = data.get("preferred_locale")

    if "public_updates_channel_id" in data:
      self.public_updates_channel_id = data.get("public_updates_channel_id")

    if "max_video_channel_users" in data:
      self.max_video_channel_users = data.get("max_video_channel_users")

    if "max_stage_video_channel_users" in data:
      self.max_stage_video_channel_users = data.get("max_stage_video_channel_users")

    if "approximate_member_count" in data:
      self.approximate_member_count = data.get("approximate_member_count")

    if "approximate_presence_count" in data:
      self.approximate_presence_count = data.get("approximate_presence_count")

    if "welcome_screen" in data:
      welcome_screen = data.get("welcome_screen")
      if isinstance(welcome_screen, dict):
        self.welcome_screen.update(welcome_screen)

    if "nsfw_level" in data:
      self.nsfw_level = data.get("nsfw_level")

    if "stickers" in data:
      stickers_all = data.get("stickers")
      if isinstance(stickers_all, list):
        for sticker_dict in stickers_all:
          if not isinstance(sticker_dict, dict):
            continue

          sticker_id = sticker_dict.get("id")
          if not isinstance(sticker_id, snowflake):
            continue

          if not sticker_id in sticker_dict:
            self.stickers[sticker_id] = Sticker()
          self.stickers[sticker_id].update(sticker_dict)

    if "premium_progress_bar_enabled" in data:
      self.premium_progress_bar_enabled = data.get("premium_progress_bar_enabled")

    if "safety_alerts_channel_id" in data:
      self.safety_alerts_channel_id = data.get("safety_alerts_channel_id")

    if "incidents_data" in data:
      incidents_data = data.get("incidents_data")
      if isinstance(incidents_data, dict):
        self.incidents_data.update(incidents_data)

    if "joined_at" in data:
      self.joined_at = data.get("joined_at")

    if "large" in data:
      self.large = data.get("large")

    if "unavailable" in data:
      self.unavailable = data.get("unavailable")

    if "member_count" in data:
      self.member_count = data.get("member_count")

    if "members" in data:
      members_all = data.get("members")
      if isinstance(members_all, list):
        for member_dict in members_all:
          if not isinstance(member_dict, dict):
            continue

          member_id = member_dict.get("id")
          if not isinstance(member_id, snowflake):
            continue

          if not member_id in member_dict:
            self.members[member_id] = GuildMember()
          self.members[member_id].update(member_dict)

    if "channels" in data:
      channels_all = data.get("channels")
      if isinstance(channels_all, list):
        for channel_dict in channels_all:
          if not isinstance(channel_dict, dict):
            continue

          channel_id = channel_dict.get("id")
          if not isinstance(channel_id, snowflake):
            continue

          if not channel_id in channel_dict:
            self.channels[channel_id] = Channel()
          self.channels[channel_id].update(channel_dict)

    if "threads" in data:
      threads_all = data.get("threads")
      if isinstance(threads_all, list):
        for thread_dict in threads_all:
          if not isinstance(thread_dict, dict):
            continue

          thread_id = thread_dict.get("id")
          if not isinstance(thread_id, snowflake):
            continue

          if not thread_id in thread_dict:
            self.threads[thread_id] = Channel()
          self.threads[thread_id].update(thread_dict)

    if "stage_instances" in data:
      stage_instances_all: list[dict] | None = data.get("stage_instances")
      if isinstance(stage_instances_all, list):
        for stage_instance_dict in stage_instances_all:
          if not isinstance(stage_instance_dict, dict):
            continue

          stage_instance_id = stage_instance_dict.get("id")
          if not isinstance(stage_instance_id, snowflake):
            continue

          if not stage_instance_id in stage_instance_dict:
            self.stage_instances[stage_instance_id] = StageInstance()
          self.stage_instances[stage_instance_id].update(stage_instance_dict)

    if "guild_scheduled_events" in data:
      guild_scheduled_events_all: list[dict] | None = data.get("guild_scheduled_events")
      if isinstance(guild_scheduled_events_all, list):
        for guild_scheduled_event_dict in guild_scheduled_events_all:
          if not isinstance(guild_scheduled_event_dict, dict):
            continue

          guild_scheduled_event_id = guild_scheduled_event_dict.get("id")
          if not isinstance(guild_scheduled_event_id, snowflake):
            continue

          if not guild_scheduled_event_id in guild_scheduled_event_dict:
            self.guild_scheduled_events[guild_scheduled_event_id] = GuildScheduledEvent()
          self.guild_scheduled_events[guild_scheduled_event_id].update(guild_scheduled_event_dict)

    if "soundboard_sounds" in data:
      soundboard_sounds_all: list[dict] | None = data.get("soundboard_sounds")
      if isinstance(soundboard_sounds_all, list):
        for soundboard_sound_dict in soundboard_sounds_all:
          if not isinstance(soundboard_sound_dict, dict):
            continue

          soundboard_sound_id = soundboard_sound_dict.get("id")
          if not isinstance(soundboard_sound_id, snowflake):
            continue

          if not soundboard_sound_id in soundboard_sound_dict:
            self.soundboard_sounds[soundboard_sound_id] = SoundboardSound()
          self.soundboard_sounds[soundboard_sound_id].update(soundboard_sound_dict)

  def delete(self, name: Literal["welcome_screen_channel", "available_tag", "role", "emoji", "sticker", "voice_state", "member", "channel", "thread", "presence", "stage_instance", "guild_scheduled_event", "soundboard_sound"], delete_key1: snowflake, delete_key2: snowflake = ""):
    if name == "welcome_screen_channel":
      if delete_key1 in self.welcome_screen.welcome_channels:
        self.welcome_screen.welcome_channels.pop(delete_key1)

    if name == "available_tag":
      if delete_key1 in self.channels:
        if delete_key2 in self.channels[delete_key1].available_tags:
          self.channels[delete_key1].available_tags.pop(delete_key2)

    if name == "role":
      if delete_key1 in self.roles:
        self.roles.pop(delete_key1)

    if name == "emoji":
      if delete_key1 in self.emojis:
        self.emojis.pop(delete_key1)

    if name == "sticker":
      if delete_key1 in self.stickers:
        self.stickers.pop(delete_key1)

    if name == "member":
      if delete_key1 in self.members:
        self.members.pop(delete_key1)

    if name == "channel":
      if delete_key1 in self.channels:
        self.channels.pop(delete_key1)

    if name == "thread":
      if delete_key1 in self.threads:
        self.threads.pop(delete_key1)

    if name == "stage_instance":
      if delete_key1 in self.stage_instances:
        self.stage_instances.pop(delete_key1)

    if name == "guild_scheduled_event":
      if delete_key1 in self.guild_scheduled_events:
        self.guild_scheduled_events.pop(delete_key1)

    if name == "soundboard_sound":
      if delete_key1 in self.soundboard_sounds:
        self.soundboard_sounds.pop(delete_key1)
#####################