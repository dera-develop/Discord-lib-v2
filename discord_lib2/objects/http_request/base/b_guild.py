from dataclasses import dataclass
from typing import Literal, ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude


from discord_lib2.objects.http_request.base import b_channel
from discord_lib2.objects.http_request.base import b_user
from discord_lib2.objects.http_request.base import b_emoji as emoji_objects

snowflake = str
image_data = str
ISO8601timestamp = str

@dataclass
class __GuildBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>"

DMNL_ALL_MESSAGES = 0
DMNL_ONLY_MENTIONS = 1

ECFL_DISABLED = 0
ECFL_MEMBERS_WITHOUT_ROLES = 1
ECFL_ALL_MEMBERS = 2

MFAL_NONE = 0
MFAL_ELEVATED = 1

VL_NONE = 0
VL_LOW = 1
VL_MEDIUM = 2
VL_HIGH = 3
VL_VERY_HIGH = 4

GARL_DEFAULT = 0
GARL_EXPLICIT = 1
GARL_SAFE = 2
GARL_AGE_RESTRICTED = 3

PT_NONE = 0
PT_TIER_1 = 1
PT_TIER_2 = 2
PT_TIER_3 = 3

SCF_SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
SCF_SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
SCF_SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
SCF_SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
SCF_SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
SCF_SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5

CT_GUILD_TEXT = 0
CT_DM = 1
CT_GUILD_VOICE = 2
CT_GROUP_DM = 3
CT_GUILD_CATEGORY = 4
CT_GUILD_ANNOUNCEMENT = 5
CT_ANNOUNCEMENT_THREAD = 10
CT_PUBLIC_THREAD = 11
CT_PRIVATE_THREAD = 12
CT_GUILD_STAGE_VOICE = 13
CT_GUILD_DIRECTORY = 14
CT_GUILD_FORUM = 15
CT_GUILD_MEDIA = 16

OM_ONBOARDING_DEFAULT = 0
OM_ONBOARDING_ADVANCED = 1

PT_MULTIPLE_CHOICE = 0
PT_DROPDOWN = 1

@dataclass
class RoleColors:
  primary_color: int
  secondary_color: int | None
  tertiary_color: int | None

@dataclass
class UnavailableGuild:
  id: snowflake
  unavailable: bool

@dataclass
class WelcomeScreenChannel:
  channel_id: snowflake
  description: str
  emoji_id: snowflake | None
  emoji_name: str | None

@dataclass
class PromptOption:
  id: snowflake
  channel_ids: list[snowflake]
  role_ids: list[snowflake]
  emoji: emoji_objects.Emoji
  title: str
  description: str | None
  emoji_id: snowflake | Exclude = Exclude()
  emoji_name : str | Exclude = Exclude()
  emoji_animated: bool | Exclude = Exclude()
  
@dataclass
class OnboardingPrompt:
  id: snowflake
  type: Literal[0, 1]
  options: list[PromptOption]
  title: str
  single_select: bool
  required: bool
  in_onboarding: bool

@dataclass
class GuildMemberUser:
  id: snowflake

@dataclass
class GuildMember:
  user: GuildMemberUser
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
  avatar_decoration_data: b_user.AvatarDecorationData
  collectibles: b_user.Collectibles

@dataclass
class GetGuild(__GuildBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildPreview(__GuildBase):
  req_url:  ClassVar[str] = "/preview"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuild(__GuildBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "patch"

  name: str
  afk_timeout: Literal[60, 300, 900, 1800, 3600]
  system_channel_flags: int
  features: list[str]
  premium_progress_bar_enabled: bool
  region: str | None
  verification_level: int | None
  default_message_nontifications: int | None
  explicit_content_filter: int | None
  afk_channel_id: snowflake | None
  icon: image_data | None
  splash: image_data | None
  discovery_splash: image_data | None
  banner: image_data | None
  system_channel_id: snowflake | None
  rules_channel_id: snowflake | None
  public_updates_channel_id: snowflake | None
  preferred_locale: str | None
  description: str | None
  safety_alerts_channel_id: snowflake | None

@dataclass
class GetGuildChannels(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildChannel(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "post"

  name: str
  type: int | None | Exclude = Exclude()
  topic: str | None | Exclude = Exclude()
  bitrate: int | None | Exclude = Exclude()
  user_limit: int | None | Exclude = Exclude()
  rate_limit_per_user: int | None | Exclude = Exclude()
  position: int | None | Exclude = Exclude()
  permission_overwrite: list[b_channel.Overwrite] | None | Exclude = Exclude()
  parent_id: snowflake | None | Exclude = Exclude()
  nsfw: bool | None | Exclude = Exclude()
  rtc_region: str | None | Exclude = Exclude()
  video_quality_mode: int | None | Exclude = Exclude()
  default_auto_archive_duration: int | None | Exclude = Exclude()
  default_reaction_emoji: b_channel.DefaultReaction | None | Exclude = Exclude()
  available_tags: list[b_channel.ForumTag] | None | Exclude = Exclude()
  default_sort_order: int | None | Exclude = Exclude()
  default_forum_layout: int | None | Exclude = Exclude()
  default_thread_rate_limit_per_user: int | None | Exclude = Exclude()

@dataclass
class ModifyGuildChannelPositions(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "patch"

  id: snowflake
  position: int | None | Exclude = Exclude()
  lock_permissions: bool | None | Exclude = Exclude()
  parent_id: snowflake | None | Exclude = Exclude()

@dataclass
class ListActiveGuildThreads(__GuildBase):
  req_url:  ClassVar[str] = "/threads/active"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ListGuildMembers(__GuildBase):
  req_url:  ClassVar[str] = "/members"
  req_type: ClassVar[str] = "get"

@dataclass
class SearchGuildMembers(__GuildBase):
  req_url:  ClassVar[str] = "/members/search"
  req_type: ClassVar[str] = "get"

@dataclass
class AddGuildMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>"
  req_type: ClassVar[str] = "put"

  access_token: str
  nick: str
  roles: list[snowflake]
  mute: bool
  deaf: bool

@dataclass
class ModifyGuildMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>"
  req_type: ClassVar[str] = "patch"

  nick: str
  roles: list[snowflake]
  mute: bool
  deaf: bool
  channel_id: snowflake
  communication_disabled_until: ISO8601timestamp
  flags: int

@dataclass
class ModifyCurrentMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/@me"
  req_type: ClassVar[str] = "patch"

  nick: str | None | Exclude = Exclude()
  banner: image_data | None | Exclude = Exclude()
  avatar: image_data | None | Exclude = Exclude()
  bio: str | None | Exclude = Exclude()

@dataclass
class ModifyCurrentUserNick(__GuildBase):
  req_url:  ClassVar[str] = "/members/@me/nick"
  req_type: ClassVar[str] = "patch"

  nick: str | None | Exclude = Exclude()

@dataclass
class AddGuildMemberRole(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>/roles/<role.id>"
  req_type: ClassVar[str] = "put"

@dataclass
class RemoveGuildMemberRole(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>/roles/<role.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class RemoveGuildMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetGuildBans(__GuildBase):
  req_url:  ClassVar[str] = "/bans"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bans/<user.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bans/<user.id>"
  req_type: ClassVar[str] = "put"

  delete_message_days: int | Exclude = Exclude()
  delete_message_seconds: int | Exclude = Exclude()

@dataclass
class RemoveGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bans/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bulk-ban"
  req_type: ClassVar[str] = "post"

  user_ids: list[snowflake]
  delete_message_seconds: int | Exclude = Exclude()

@dataclass
class GetGuildRoles(__GuildBase):
  req_url:  ClassVar[str] = "/roles"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildRole(__GuildBase):
  req_url:  ClassVar[str] = "/roles/<role.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildRoleMemberCounts(__GuildBase):
  req_url:  ClassVar[str] = "/roles/member-counts"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildRole(__GuildBase):
  req_url:  ClassVar[str] = "/roles"
  req_type: ClassVar[str] = "post"

  name: str
  permissions: str
  color: int
  colors: RoleColors
  hoist: bool
  icon: image_data | None
  unicode_emoji: str | None
  mentionable: bool

@dataclass
class ModifyGuildRolePositions(__GuildBase):
  req_url:  ClassVar[str] = "/roles"
  req_type: ClassVar[str] = "patch"

  id: snowflake
  position: int | None | Exclude = Exclude()

@dataclass
class ModifyGuildRole(__GuildBase):
  req_url:  ClassVar[str] = "/roles/<role.id>"
  req_type: ClassVar[str] = "patch"

  name: str
  permissions: str
  color: int
  colors: RoleColors
  hoist: bool
  icon: image_data
  unicode_emoji: str
  mentionable: bool

@dataclass
class DeleteGuildRole(__GuildBase):
  req_url:  ClassVar[str] = "/roles/<role.io>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetGuildPruneCount(__GuildBase):
  req_url:  ClassVar[str] = "/prune"
  req_type: ClassVar[str] = "get"

@dataclass
class BeginGuildPrune(__GuildBase):
  req_url:  ClassVar[str] = "/prune"
  req_type: ClassVar[str] = "post"

  days: int
  compute_prune_count: bool
  include_roles: list[snowflake]
  reason: str | Exclude = Exclude()

@dataclass
class GetGuildVoiceRegions(__GuildBase):
  req_url:  ClassVar[str] = "/regions"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildInvites(__GuildBase):
  req_url:  ClassVar[str] = "/invites"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildIntegrations(__GuildBase):
  req_url:  ClassVar[str] = "/integrations"
  req_type: ClassVar[str] = "get"

@dataclass
class DeleteGuildIntegration(__GuildBase):
  req_url:  ClassVar[str] = "/integrations/<integration.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetGuildWidgetSettings(__GuildBase):
  req_url:  ClassVar[str] = "/widget"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildWidget(__GuildBase):
  req_url:  ClassVar[str] = "/widget"
  req_type: ClassVar[str] = "patch"

@dataclass
class GetGuildWidget(__GuildBase):
  req_url:  ClassVar[str] = "/widget.json"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildVanityURL(__GuildBase):
  req_url:  ClassVar[str] = "/vanity-url"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildWidgetImage(__GuildBase):
  req_url:  ClassVar[str] = "/widget.png"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildWelcomeScreen(__GuildBase):
  req_url:  ClassVar[str] = "/welcome-screen"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildWelcomeScreen(__GuildBase):
  req_url:  ClassVar[str] = "/welcome-screen"
  req_type: ClassVar[str] = "patch"

  enabled: bool
  welcome_channels: list[WelcomeScreenChannel]
  description: str

@dataclass
class GetGuildOnboarding(__GuildBase):
  req_url:  ClassVar[str] = "/onboarding"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildOnboarding(__GuildBase):
  req_url:  ClassVar[str] = "/onboarding"
  req_type: ClassVar[str] = "put"

  prompts: list[OnboardingPrompt]
  default_channel_ids: list[snowflake]
  enabled: bool
  mode: Literal[0, 1]

@dataclass
class ModifyGuildIncidentActions(__GuildBase):
  req_url:  ClassVar[str] = "/incident-actions"
  req_type: ClassVar[str] = "put"

  invites_disabled_until: ISO8601timestamp | None | Exclude = Exclude()
  dms_disabled_until: ISO8601timestamp | None | Exclude = Exclude()


