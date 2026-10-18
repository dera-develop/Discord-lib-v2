"""
Gatewayイベントの構造体（受信側）
"""
from dataclasses import dataclass, field
from typing import Any

from discord_lib2.objects.http_request.body import b_guild

snowflake = str
ISO8601timestamp = str

@dataclass
class User:
  @dataclass
  class AvatarDecorationData:
    asset: str | None = None
    sku_id: snowflake | None = None
  @dataclass
  class Collectibles:
    @dataclass
    class Nameplate:
      sku_id: snowflake | None = None
      asset: str | None = None
      label: str | None = None
      palette: str | None = None
    nameplate: Nameplate | None = None
  @dataclass
  class PrimaryGuild:
    identity_guild_id: snowflake | None = None
    identity_enabled: bool | None = None
    tag: str | None = None
    badge: str | None = None
  id: snowflake
  username: str
  discriminator: str
  global_name: str | None = None
  avatar: str | None = None
  bot: bool | None = None
  system: bool | None = None
  mfa_enabled: bool | None = None
  banner: str | None = None
  accent_color: int | None = None
  locale: str | None = None
  verified: bool | None = None
  email: str | None = None
  flags: int | None = None
  premium_type: int | None = None
  public_flags: int | None = None
  avatar_decoration_data: AvatarDecorationData | None = None
  collectibles: Collectibles | None = None
  primary_guild: PrimaryGuild | None = None

@dataclass
class Ready:
  @dataclass
  class Application:
    id: snowflake | None = None
    flags: int | None = None
    flags_new: str | None = None

  v: int
  user: User
  guilds: list[b_guild.UnavailableGuild] = field(default_factory=list)
  session_id: str | None = None
  resume_gateway_url: str | None = None
  application: Application = field(default_factory=Application)
  shard: list[list[int]] | None = None

@dataclass
class Role:
  @dataclass
  class Colors:
    primary_color: int | None = None
    secondary_color: int | None = None
    tertiary_color: int | None = None
  @dataclass
  class Tags:
    bot_id: snowflake | None = None
    integration_id: snowflake | None = None
    premium_subscriber: None = None
    subscription_listing_id: snowflake | None = None
    available_for_purchase: None = None
    guild_connections: None = None
  id: snowflake
  name: str | None = None
  color: int | None = None
  colors: Colors = field(default_factory=Colors)
  hoist: bool | None = None
  icon: str | None = None
  unicode_emoji: str | None = None
  position: int | None = None
  permissions: str | None = None
  managed: bool | None = None
  mentionable: bool | None = None
  tags: Tags | None = None
  flags: int | None = None

@dataclass
class Emoji:
  id: snowflake | None = None
  name: str | None = None
  roles: list[snowflake] | None = None
  user: User | None = None
  require_colons: bool | None = None
  managed: bool | None = None
  animated: bool | None = None
  available: bool | None = None

@dataclass
class Sticker:
  id: snowflake | None = None
  pack_id: snowflake | None = None
  name: str | None = None
  description: str | None = None
  tags: str | None = None
  type: int | None = None
  format_type: int | None = None
  available: bool | None = None
  guild_id: snowflake | None = None
  user: User | None = None
  sort_value: int | None = None

@dataclass
class Guild:
  @dataclass
  class WelcomeScreen:
    @dataclass
    class WelcomeScreenChannel:
      channel_id: snowflake | None = None
      description: str | None = None
      emoji_id: snowflake | None = None
      emoji_name: str | None = None
    description: str | None = None
    welcome_channels: list[WelcomeScreenChannel] = field(default_factory=list)
  @dataclass
  class IncidentsData:
    invites_disabled_until: ISO8601timestamp | None = None
    dms_disabled_until: ISO8601timestamp | None = None
    dm_spam_detected_at: ISO8601timestamp | None = None
    raid_detected_at: ISO8601timestamp | None = None
  id: snowflake
  name: str
  owner_id: snowflake
  afk_timeout: int
  verification_level: int
  default_message_notifications: int
  explicit_content_filter: int
  mfa_level: int
  system_channel_flags: int
  premium_tier: int
  preferred_locale: str
  nsfw_level: int
  premium_progress_bar_enabled: bool
  icon: str | None = None
  icon_hash: str | None = None
  splash: str | None = None
  discovery_splash: str | None = None
  owner: bool | None = None
  permissions: str | None = None
  region: str | None = None
  afk_channel_id: snowflake | None = None
  widget_enabled: bool | None = None
  widget_channel_id: snowflake | None = None
  roles: list[Role] = field(default_factory=list)
  emojis: list[Emoji] = field(default_factory=list)
  features: list[str] = field(default_factory=list)
  application_id: snowflake | None = None
  system_channel_id: snowflake | None = None
  rules_channel_id: snowflake | None = None
  max_presences: int | None = None
  max_members: int | None = None
  vanity_url_code: str | None = None
  description: str | None = None
  banner: str | None = None
  premium_subscription_count: int | None = None
  public_updates_channel_id: snowflake | None = None
  max_video_channel_users: int | None = None
  max_stage_video_channel_users: int | None = None
  approximate_member_count: int | None = None
  approximate_presence_count: int | None = None
  welcome_screen: WelcomeScreen | None = None
  stickers: list[Sticker] | None = None
  safety_alerts_channel_id: snowflake | None = None
  incidents_data: IncidentsData | None = None

@dataclass
class GuildMember:
  deaf: bool
  mute: bool
  flags: int
  user: User | None = None
  nick: str | None = None
  avatar: str | None = None
  banner: str | None = None
  roles: list[snowflake] = field(default_factory=list)
  joined_at: ISO8601timestamp | None = None
  premium_since: ISO8601timestamp | None = None
  pending: bool | None = None
  permissions: str | None = None
  communication_disabled_until: ISO8601timestamp | None = None
  avatar_decoration_data: User.AvatarDecorationData | None = None
  collectibles: User.Collectibles | None = None

@dataclass
class GuildMemberUpdate(GuildMember):
  guild_id: snowflake | None = None

@dataclass
class VoiceState:
  user_id: snowflake
  session_id: str
  deaf: bool
  mute: bool
  self_deaf: bool
  self_mute: bool
  self_video: bool
  suppress: bool
  guild_id: snowflake | None = None
  channel_id: snowflake | None = None
  member: GuildMember | None = None
  self_stream: bool | None = None
  request_to_speak_timestamp: ISO8601timestamp | None = None

@dataclass
class Channel:
  @dataclass
  class OverWrite:
    id: snowflake | None = None
    type: int | None = None
    allow: str | None = None
    deny: str | None = None
  @dataclass
  class ThreadMetadata:
    archived: bool | None = None
    auto_archive_duration: int | None = None
    archive_timestamp: ISO8601timestamp | None = None
    locked: bool | None = None
    invitable: bool | None = None
    create_timestamp: ISO8601timestamp | None = None
  @dataclass
  class ThreadMember:
    id: snowflake | None = None
    user_id: snowflake | None = None
    join_timestamp: ISO8601timestamp | None = None
    flags: int | None = None
    member: GuildMember | None = None
  @dataclass
  class ForumTag:
    id: snowflake | None = None
    name: str | None = None
    moderated: bool | None = None
    emoji_id: snowflake | None = None
    emoji_name: str | None = None
  @dataclass
  class DefaultReaction:
    emoji_id: snowflake | None = None
    emoji_name: str | None = None
  id: snowflake
  type: int
  guild_id: snowflake | None = None
  position: int | None = None
  permission_overwrites: list[OverWrite] | None = None
  name: str | None = None
  topic: str | None = None
  nsfw: bool | None = None
  last_message_id: snowflake | None = None
  bitrate: int | None = None
  user_limit: int | None = None
  rate_limit_per_user: int | None = None
  recipients: list[User] | None = None
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
  thread_metadata: ThreadMetadata | None = None
  member: ThreadMember | None = None
  default_auto_archive_duration: int | None = None
  permissions: str | None = None
  app_permissions: str | None = None
  flags: int | None = None
  total_message_sent: int | None = None
  available_tags: list[ForumTag] | None = None
  applied_tags: list[snowflake] | None = None
  default_reaction_emoji: DefaultReaction | None = None
  default_thread_rate_limit_per_user: int | None = None
  default_sort_order: int | None = None
  default_forum_layout: int | None = None

@dataclass
class PresenceUpdate:
  @dataclass
  class Activity:
    @dataclass
    class A_Timestamps:
      start: int | None = None
      end: int | None = None
    @dataclass
    class A_Emoji:
      name: str
      id: snowflake | None = None
      animated: bool | None = None
    @dataclass
    class A_Party:
      id: str | None = None
      size: list[int] | None = None
    @dataclass
    class A_Assets:
      large_image: str | None = None
      large_text: str | None = None
      large_url: str | None = None
      small_image: str | None = None
      small_text: str | None = None
      small_url: str | None = None
      invite_cover_image: str | None = None
    @dataclass
    class A_Secrets:
      join: str | None = None
      spectate: str | None = None
      match: str | None = None
    @dataclass
    class A_Buttons:
      label: str | None = None
      url: str | None = None
    name: str
    type: int
    created_at: int
    url: str | None = None
    timestamps: A_Timestamps | None = None
    application_id: snowflake | None = None
    status_display_type: int | None = None
    details: str | None = None
    details_url: str | None = None
    state: str | None = None
    state_url: str | None = None
    emoji: A_Emoji | None = None
    party: A_Party | None = None
    assets: A_Assets | None = None
    secrets: A_Secrets | None = None
    instance: bool | None = None
    flags: int | None = None
    buttons: list[A_Buttons] | None = None
  @dataclass
  class ClientStatus:
    pasdesktop: str | None = None
    mobile: str | None = None
    web: str | None = None
    vr: str | None = None
  user: User
  guild_id: snowflake
  status: str
  activities: list[Activity] = field(default_factory=list)
  client_status: ClientStatus = field(default_factory=ClientStatus)

@dataclass
class StageInstance:
  id: snowflake | None = None
  guild_id: snowflake | None = None
  channel_id: snowflake | None = None
  topic: str | None = None
  privacy_level: int | None = None
  discoverable_disabled: bool | None = None
  guild_scheduled_event_id: snowflake | None = None

@dataclass
class GuildScheduledEvent:
  @dataclass
  class EntityMetadata:
    location: str | None = None
  @dataclass
  class RecurrenceRule:
    @dataclass
    class NWeekday:
      n: int | None = None
      day: int | None = None
    start: ISO8601timestamp | None = None
    end: ISO8601timestamp | None = None
    frequency: int | None = None
    interval: int | None = None
    by_weekday: list[int] | None = None
    by_n_weekday: list[NWeekday] | None = None
    by_month: list[int] | None = None
    by_month_day: list[int] | None = None
    by_year_day: list[int] | None = None
    count: int | None = None
  id: snowflake
  guild_id: snowflake
  name: str
  scheduled_start_time: ISO8601timestamp
  privacy_level: int
  status: int
  entity_type: int
  channel_id: snowflake | None = None
  creator_id: snowflake | None = None
  description: str | None = None
  scheduled_end_time: ISO8601timestamp | None = None
  entity_id: snowflake | None = None
  entity_metadata: EntityMetadata | None = None
  creator: User | None = None
  user_count: int | None = None
  image: str | None = None
  recurrence_rule: RecurrenceRule | None = None

@dataclass
class SoundboardSound:
  name: str
  sound_id: snowflake
  volume: float
  available: bool
  emoji_id: snowflake | None = None
  emoji_name: str | None = None
  guild_id: snowflake | None = None
  user: User | None = None

@dataclass
class GuildCreate(Guild):
  joined_at: ISO8601timestamp | None = None
  large: bool | None = None
  unavailable: bool | None = None
  member_count: int | None = None
  voice_states: list[VoiceState] = field(default_factory=list)
  members: list[GuildMember] = field(default_factory=list)
  channels: list[Channel] = field(default_factory=list)
  threads: list[Channel] = field(default_factory=list)
  presences: list[PresenceUpdate] = field(default_factory=list)
  stage_instances: list[StageInstance] = field(default_factory=list)
  guild_scheduled_events: list[GuildScheduledEvent] = field(default_factory=list)
  soundboard_sounds: list[SoundboardSound] = field(default_factory=list)

@dataclass
class ThreadListSync:
  guild_id: snowflake
  channel_ids: list[snowflake] | None = None
  threads: list[Channel] = field(default_factory=list)
  members: list[Channel.ThreadMember] = field(default_factory=list)

@dataclass
class ThreadMembersUpdate:
  id: snowflake
  guild_id: snowflake
  member_count: int
  added_members: list[Channel.ThreadMember] | None = None
  removed_member_ids: list[snowflake] | None = None

@dataclass
class ChannelPinsUpdate:
  channel_id: snowflake
  guild_id: snowflake | None = None
  last_pin_timestamp: ISO8601timestamp | None = None

@dataclass
class GuildMembersChunk:
  guild_id: snowflake
  chunk_index: int
  chunk_count: int
  members: list[GuildMember]  = field(default_factory=list)
  not_found: list[Any] | None = None
  presences: list[PresenceUpdate] | None = None
  nonce: str | None = None

@dataclass
class GuildMemberRemove:
  guild_id: snowflake
  user: User

@dataclass
class GuildScheduledEventUserAdd:
  guild_scheduled_event_id: snowflake
  user_id: snowflake
  guild_id: snowflake

@dataclass
class GuildScheduledEventUserRemove:
  guild_scheduled_event_id: snowflake
  user_id: snowflake
  guild_id: snowflake

@dataclass
class GuildEmojisUpdate:
  guild_id: snowflake | None = None
  emojis: list[Emoji] = field(default_factory=list)

@dataclass
class GuildStickersUpdate:
  guild_id: snowflake
  stickers: list[Sticker] = field(default_factory=list)

@dataclass
class GuildBanEvent:
  guild_id: snowflake
  user: User

@dataclass
class GuildSoundboardSoundDelete:
  sound_id: snowflake | None = None
  guild_id: snowflake | None = None

@dataclass
class GuildSoundboardSoundsUpdate:
  soundboard_sounds: list[SoundboardSound] = field(default_factory=list)
  guild_id: snowflake | None = None

@dataclass
class Integration:
  @dataclass
  class Account:
    id: str
    name: str
  @dataclass
  class Application:
    id: snowflake
    name: str
    description: str
    icon: str | None = None
    bot: User | None = None
  id: snowflake
  name: str
  type: str
  enabled: bool
  account: Account
  syncing: bool | None = None
  role_id: snowflake | None = None
  enable_emoticons: bool | None = None
  expire_behavior: int | None = None
  expire_grace_period: int | None = None
  user: User | None = None
  synced_at: ISO8601timestamp | None = None
  subscriber_count: int | None = None
  revoked: bool | None = None
  application: Application | None = None
  scopes: list[str] | None = None

@dataclass
class IntegrationEvent(Integration):
  guild_id: snowflake | None = None

@dataclass
class IntegrationDelete:
  id: snowflake | None = None
  guild_id: snowflake | None = None
  application_id: snowflake | None = None

@dataclass
class Team:
  @dataclass
  class Member:
    membership_state: int
    team_id: snowflake
    user: User
    role: str
  icon: str | None = None
  id: snowflake | None = None
  members: list[Member] = field(default_factory=list)
  name: str | None = None
  owner_user_id: snowflake | None = None

@dataclass
class Application:
  @dataclass
  class InstallParams:
    scopes: list[str]
    permissions: str
  id: snowflake
  name: str
  description: str
  bot_public: bool
  bot_require_code_grant: bool
  verify_key: str
  icon: str | None = None
  rpc_origins: list[str] | None = None
  bot: User | None = None
  terms_of_service_url: str | None = None
  privacy_policy_url: str | None = None
  owner: User | None = None
  team: Team | None = None
  guild_id: snowflake | None = None
  guild: Guild | None = None
  primary_sku_id: snowflake | None = None
  slug: str | None = None
  cover_image: str | None = None
  flags: int | None = None
  flags_new: str | None = None
  approximate_guild_count: int | None = None
  approximate_user_install_count: int | None = None
  approximate_user_authorization_count: int | None = None
  redirect_uris: list[str] | None = None
  interactions_endpoint_url: str | None = None
  role_connections_verification_url: str | None = None
  event_webhooks_url: str | None = None
  event_webhooks_status: int | None = None
  event_webhooks_types: list[str] | None = None
  tags: list[str] | None = None
  install_params: InstallParams | None = None
  integration_types_config: dict[Any, Any] | None = None
  custom_install_url: str | None = None

@dataclass
class PollMedia:
  text: str | None = None
  emoji: Emoji | None = None

@dataclass
class PollAnswer:
  answer_id: int | None = None
  poll_media: PollMedia | None = None

@dataclass
class Poll:
  @dataclass
  class Results:
    @dataclass
    class AnswerCount:
      id: int
      count: int
      me_voted: bool
    is_finalized: bool
    answer_counts: list[AnswerCount]
  question: PollMedia
  answers: list[PollAnswer]
  expiry: ISO8601timestamp | None = None
  allow_multiselect: bool | None = None
  layout_type: int | None = None
  results: Results | None = None

@dataclass
class PartialMessage:
  id: snowflake
  content: str
  author: User
  timestamp: ISO8601timestamp

@dataclass
class MiniMessage(PartialMessage):
  @dataclass
  class Attachment:
    id: snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    title: str | None = None
    description: str | None = None
    content_type: str | None = None
    height: int | None = None
    width: int | None = None
    placeholder: str | None = None
    placeholder_version: int | None = None
    ephemeral: bool | None = None
    duration_secs: float | None = None
    waveform: str | None = None
    flags: int | None = None
    clip_participants: list[User] | None = None
    clip_created_at: ISO8601timestamp | None = None
    application: Application | None = None
  @dataclass
  class Embed:
    @dataclass
    class Video:
      url: str | None = None
      proxy_url: str | None = None
      height: int | None = None
      width: int | None = None
      content_type: str | None = None
      placeholder: str | None = None
      placeholder_version: int | None = None
      description: str | None = None
      flags: int | None = None
    @dataclass
    class Image:
      url: str
      proxy_url: str | None = None
      height: int | None = None
      width: int | None = None
      content_type: str | None = None
      placeholder: str | None = None
      placeholder_version: int | None = None
      description: str | None = None
      flags: int | None = None
    @dataclass
    class Provider:
      name: str | None = None
      url: str | None = None
    @dataclass
    class Author:
      name: str
      url: str | None = None
      icon_url: str | None = None
      proxy_icon_url: str | None = None
    @dataclass
    class Footer:
      text: str
      icon_url: str | None = None
      proxy_icon_url: str | None = None
    @dataclass
    class Field:
      name: str
      value: str
      inline: bool | None = None
    title: str | None = None
    type: str | None = None
    description: str | None = None
    url: str | None = None
    timestamp: ISO8601timestamp | None = None
    color: int | None = None
    footer: Footer | None = None
    image: Image | None = None
    thumbnail: Image | None = None
    video: Video | None = None
    provider: Provider | None = None
    author: Author | None = None
    fields: list[Field] | None = None
    flags: int | None = None
  @dataclass
  class StickerItem:
    id: snowflake
    name: str
    format_type: int
  type: int
  embeds: list[Embed] | None = None
  attachments: list[Attachment] | None = None
  edited_timestamp: ISO8601timestamp | None = None
  flags: int | None = None
  mentions: list[User] | None = None
  mention_roles: list[snowflake] | None = None
  stickers: list[Sticker] | None = None
  sticker_items: list[StickerItem] | None = None
  components: list[Any] | None = None

@dataclass
class Message(MiniMessage):
  @dataclass
  class ChannelMention:
    id: snowflake
    guild_id: snowflake
    type: int
    name: str
  @dataclass
  class Reaction:
    @dataclass
    class ReactionDetails:
      burst: int
      normal: int
    count: int
    count_details: ReactionDetails
    me: bool
    me_burst: bool
    emoji: Emoji
    burst_colors: list[Any]
  @dataclass
  class MActivity:
    type: int
    party_id: str | None = None
  @dataclass
  class Reference:
    type: int | None = None
    message_id: snowflake | None = None
    channel_id: snowflake | None = None
    guild_id: snowflake | None = None
    fail_if_not_exists: bool | None = None
  @dataclass
  class Snapshot:
    message: MiniMessage
  @dataclass
  class InteractionMetadata:
    id: snowflake
    type: int
    user: User
    authorizing_integration_owners: dict[Any, Any]
    original_response_message_id: snowflake | None = None
    target_user: User | None = None
    target_message_id: snowflake | None = None
  @dataclass
  class Interaction:
    id: snowflake
    type: int
    name: str
    user: User
    member: GuildMember | None = None
  @dataclass
  class RoleSubscriptionData:
    role_subscription_listing_id: snowflake
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool
  @dataclass
  class ResolvedData:
    users: dict[snowflake, User] | None = None
    members: dict[snowflake, GuildMember] | None = None
    roles: dict[snowflake, Role] | None = None
    channels: dict[snowflake, Channel] | None = None
    messages: dict[snowflake, dict] | None = None
    attachments: dict[snowflake, MiniMessage.Attachment] | None = None
  @dataclass
  class Call:
    participants: list[snowflake]
    ended_timestamp: ISO8601timestamp | None = None
  @dataclass
  class SharedClientTheme:
    colors: list[str]
    gradient_angle: int
    base_mix: int
    base_theme: int | None = None
  channel_id: snowflake | None = None
  tts: bool | None = None
  mention_everyone: bool | None = None
  mention_channels: list[ChannelMention] | None = None
  reactions: list[Reaction] | None = None
  nonce: int | str | None = None
  pinned: bool | None = None
  webhook_id: snowflake | None = None
  activity: MActivity | None = None
  application: Application | None = None
  application_id: snowflake | None = None
  message_reference: Reference | None = None
  message_snapshots: list[Snapshot] | None = None
  referenced_message: PartialMessage | None = None
  interaction_metadata: InteractionMetadata | None = None
  interaction: Interaction | None = None
  thread: Channel | None = None
  position: int | None = None
  role_subscription_data: RoleSubscriptionData | None = None
  resolved: ResolvedData | None = None
  poll: Poll | None = None
  call: Call | None = None
  shared_client_theme: SharedClientTheme | None = None

@dataclass
class MessageCreateUpdate(Message):
  guild_id: snowflake | None = None
  member: GuildMember | None = None
  mentions: list[User] | None = None
  channel_type: int | None = None

@dataclass
class MessageDelete:
  id: snowflake
  channel_id: snowflake
  guild_id: snowflake | None = None

@dataclass
class MessageDeleteBulk:
  ids: list[snowflake]
  channel_id: snowflake
  guild_id: snowflake | None = None

@dataclass
class MessageReactionAdd:
  user_id: snowflake
  channel_id: snowflake
  message_id: snowflake
  emoji: Emoji
  burst: bool
  type: int
  guild_id: snowflake | None = None
  member: GuildMember | None = None
  message_author_id: snowflake | None = None
  burst_colors: list[str] | None = None

@dataclass
class MessageReactionRemove:
  user_id: snowflake
  channel_id: snowflake
  message_id: snowflake
  emoji: Emoji
  burst: bool
  type: int
  guild_id: snowflake | None = None

@dataclass
class MessageReactionRemoveAll:
  channel_id: snowflake
  message_id: snowflake
  guild_id: snowflake | None = None

@dataclass
class MessageReactionRemoveEmoji:
  channel_id: snowflake
  message_id: snowflake
  emoji: Emoji
  guild_id: snowflake | None = None

@dataclass
class InviteCreate:
  channel_id: snowflake
  code: str
  created_at: ISO8601timestamp
  max_age: int
  max_uses: int
  temporary: bool
  uses: int

  guild_id: snowflake | None = None
  inviter: User | None = None
  target_type: int | None = None
  target_user: User | None = None
  target_application: Application | None = None
  expires_at: ISO8601timestamp | None = None
  role_ids: list[snowflake] | None = None

@dataclass
class InviteDelete:
  channel_id: snowflake
  code: str
  guild_id: snowflake | None = None

@dataclass
class Entitlement:
  id: snowflake
  sku_id: snowflake
  application_id: snowflake
  type: int
  deleted: bool
  user_id: snowflake | None = None
  starts_at: ISO8601timestamp | None = None
  ends_at: ISO8601timestamp | None = None
  guild_id: snowflake | None = None
  consumed: bool | None = None

@dataclass
class Interaction:
  @dataclass
  class ResolvedData:
    users: dict[snowflake, User] | None=None
    members: dict[snowflake, GuildMember] | None=None
    roles: dict[snowflake, Role] | None=None
    channels: dict[snowflake, Channel] | None=None
    messages: dict[snowflake, Message] | None=None
    attachments: dict[snowflake, Message.Attachment] | None=None
  id: snowflake
  application_id: snowflake
  type: int
  token: str
  version: int
  app_permissions: str
  entitlements: list[Entitlement]
  authorizing_integration_owners: dict[Any, Any]
  attachment_size_limit: int
  guild: Guild | None = None
  guild_id: snowflake | None = None
  channel: Channel | None = None
  channel_id: snowflake | None = None
  member: GuildMember | None = None
  user: User | None = None
  message: Message | None = None
  locale: str | None = None
  guild_locale: str | None = None
  context: int | None = None

@dataclass
class PingInteraction(Interaction):
  data: None = None

@dataclass
class ApplicationCommandAutocompleteInteraction(Interaction):
  @dataclass
  class ApplicationCommand:
    id: snowflake = ""
    name: str = ""
    type: int = -1
    resolved: Interaction.ResolvedData | None=None
    options: list = field(default_factory=list)
    guild_id: snowflake | None=None
    target_id: snowflake | None=None
  data: ApplicationCommand = field(default_factory=ApplicationCommand)

@dataclass
class ApplicationCommandInteraction(Interaction):
  @dataclass
  class ApplicationCommand:
    id: snowflake = ""
    name: str = ""
    type: int = -1
    resolved: Interaction.ResolvedData | None=None
    options: list = field(default_factory=list)
    guild_id: snowflake | None=None
    target_id: snowflake | None=None
  data: ApplicationCommand = field(default_factory=ApplicationCommand)

@dataclass
class MessageComponentInteraction(Interaction):
  @dataclass
  class MessageComponent:
    custom_id: str = ""
    component_type: int = -1
    values: list | None=None #TODO
    resolved: Interaction.ResolvedData | None=None
  data: MessageComponent = field(default_factory=MessageComponent)

@dataclass
class ModulSubmitInteraction(Interaction):
  @dataclass
  class ModalSubmit:
    custom_id: str = ""
    components: list = field(default_factory=list)
    resolved: Interaction.ResolvedData | None=None
  data: ModalSubmit = field(default_factory=ModalSubmit)

@dataclass
class WebhooksUpdate:
  guild_id: snowflake
  channel_id: snowflake

@dataclass
class GuildRoleEvent:
  guild_id: snowflake
  role: Role

@dataclass
class GuildRoleDelete:
  guild_id: snowflake
  role_id: snowflake

@dataclass
class TypingStart:
  channel_id: snowflake
  user_id: snowflake
  timestamp: int
  guild_id: snowflake | None = None
  member: GuildMember | None = None

@dataclass
class VoiceChannelEffectSend:
  channel_id: snowflake
  guild_id: snowflake
  user_id: snowflake
  emoji: Emoji | None = None
  animation_type: int | None = None
  animation_id: int | None = None
  sound_id: snowflake | int | None = None
  sound_volume: float | None = None

@dataclass
class VoiceChannelStartTimeUpdate:
  id: snowflake
  guild_id: snowflake
  voice_start_time: int | None = None

@dataclass
class VoiceChannelStatusUpdate:
  id: snowflake
  guild_id: snowflake
  status: str | None

@dataclass
class VoiceServerUpdate:
  token: str
  guild_id: snowflake
  endpoint: str | None

@dataclass
class GuildMemberAdd(GuildMember):
  guild_id: snowflake | None = None