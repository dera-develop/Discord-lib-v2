snowflake = str
ISO8601timestamp = str

#########################################################################################
# User Objects
#########################################################################################
class UserObjectPrimaryGuild:
  identity_guild_id: snowflake | None
  identity_enaabled: bool | None
  tag: str | None
  badge: str | None

class UserObjectAvatarDecorationData:
  asset: str
  sku_id: snowflake

class UserObjectNameplate:
  sku_id: snowflake
  asset: str
  label: str
  palette: str

class UserObjectCollectibles:
  nameplate: UserObjectNameplate

class UserObject:
  id: snowflake
  username: str
  discriminator: str
  global_name: str | None
  avatar: str | None
  bot: bool | None
  system: bool | None
  mfa_enabled: bool | None
  banner: str | None
  accent_color: int | None
  locale: str | None
  verified: bool | None
  email: str | None
  flags: int | None
  premium_type: int | None
  public_flags: int | None
  avatar_decoration_data: UserObjectAvatarDecorationData | None
  collectibles: UserObjectCollectibles | None
  primary_guild: UserObjectPrimaryGuild | None

class User:
  user: UserObject | None = None
  joined_guilds: list[snowflake] | None = None

#########################################################################################
# Channel Objects
#########################################################################################
class GuildObjectGuildMember:
  user: User
  nick: str
  avatar: str
  banner: str
  roles: list[snowflake]
  joined_at: ISO8601timestamp
  premium_since: ISO8601timestamp
  deaf: bool
  mute: bool
  flags: int
  pending: bool
  permissions: str
  communication_disabled_until: ISO8601timestamp
  avatar_decoration_data: UserObjectAvatarDecorationData
  collectibles: UserObjectCollectibles

class ChannelObjectOverwrite:
  id: snowflake
  type: int
  allow: str
  deny: str

class ChannelObjectThreadMetadata:
  archived: bool
  auto_archive_duration: int
  archive_timestamp: ISO8601timestamp
  locked: bool
  invitable: bool | None
  create_timestamp: ISO8601timestamp | None

class ChannelObjectThreadMember:
  id: snowflake | None
  user_id: snowflake | None
  join_timestamp: ISO8601timestamp
  flags: int
  member: GuildObjectGuildMember | None

class ChannelObjectForumTag:
  id: snowflake
  name: str
  moderated: bool
  emoji_id: snowflake | None
  emoji_name: str | None

class ChannelObjectDefaultReaction:
  emoji_id: snowflake | None
  emoji_name: str | None

class ChannelObject:
  id: snowflake
  type: int
  guild_id: snowflake | None
  position: int | None
  permission_overwrites: list[ChannelObjectOverwrite]
  name: str | None
  topic: str | None
  nsfw: bool | None
  last_message_id: snowflake | None
  bitrate: int | None
  user_limit: int | None
  rate_limit_per_user: int | None
  recipients: list[UserObject] | None
  icon: str | None
  awner_id: snowflake | None
  application_id: snowflake | None
  managed: bool | None
  parent_id: snowflake | None
  last_pin_timestamp: ISO8601timestamp | None
  rtc_region: str | None
  video_quality_mode: int | None
  message_count: int | None
  member_count: int | None
  thread_metadata: ChannelObjectThreadMetadata | None
  member: ChannelObjectThreadMember | None
  default_auto_archive_duration: int
  permissions: str
  app_permissions: str
  flags: int
  total_message_sent: int
  available_tags: list[ChannelObjectForumTag]
  applied_tags: list[snowflake]
  default_reaction_emoji: ChannelObjectDefaultReaction
  default_thread_rate_limit_per_user: int
  default_sort_order: int
  default_forum_layout: int

class Guild:
  channels: dict[snowflake, ChannelObject]
  users: dict[snowflake, UserObject]

#########################################################################################

class Data:
  users: dict[snowflake, User]
  guilds: dict[snowflake, Guild]

class DataCacheVault:
  data: Data
  additional = {}