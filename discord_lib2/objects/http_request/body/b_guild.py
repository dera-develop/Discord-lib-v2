from dataclasses import dataclass
from typing import Literal, ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base


from discord_lib2.objects.http_request.body import b_channel
from discord_lib2.objects.http_request.body import b_user
from discord_lib2.objects.http_request.body import b_emoji as emoji_objects

from discord_lib2.objects.http_request.format_checker import format_checker, PayloadFormatError
from discord_lib2.objects import locales

snowflake = str
image_data = str
ISO8601timestamp = str
EXCLUDE = Exclude()

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

SOT_LATEST_ACTIVITY = 0
SOT_CREATION_DATE = 1

FLT_NOT_SET = 0
FLT_LIST_VIEW = 1
FLT_GALLERY_VIEW = 2

GARL_DEFAULT = 0
GARL_EXPLICIT = 1
GARL_SAFE = 2
GARL_AGE_RESTRICTED = 3

PT_NONE = 0
PT_TIER_1 = 1
PT_TIER_2 = 2
PT_TIER_3 = 3

PT_MULTIPLE_CHOICE = 0
PT_DROPDOWN = 1

SCF_SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
SCF_SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
SCF_SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
SCF_SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
SCF_SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
SCF_SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5

OM_ONBOARDING_DEFAULT = 0
OM_ONBOARDING_ADVANCED = 1

PT_MULTIPLE_CHOICE = 0
PT_DROPDOWN = 1

FC_VERIFICATION_LEVEL = (VL_NONE, VL_LOW, VL_MEDIUM, VL_HIGH, VL_VERY_HIGH)
FC_DEFAULT_MESSAGE_NONTIFICATION_LEVEL = (DMNL_ALL_MESSAGES, DMNL_ONLY_MENTIONS)
FC_EXPLICIT_CONTENT_FILTER_LEVEL = (ECFL_DISABLED, ECFL_MEMBERS_WITHOUT_ROLES, ECFL_ALL_MEMBERS)
FC_AFK_TIMEOUT = (60, 300, 900, 1800, 3600)
FC_SORT_ORDER_TYPE = (SOT_LATEST_ACTIVITY, SOT_CREATION_DATE)
FC_FORUM_LAYOUT_TYPES = (FC_DEFAULT_MESSAGE_NONTIFICATION_LEVEL, FLT_LIST_VIEW, FLT_GALLERY_VIEW)
FC_PROMPT_TYPE = (PT_MULTIPLE_CHOICE, PT_DROPDOWN)
FC_ONBOARDING_MODE = (OM_ONBOARDING_DEFAULT, OM_ONBOARDING_ADVANCED)

@dataclass
class __GuildBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>"

@dataclass
class RoleColors(Base):
  primary_color: int
  secondary_color: int | None
  tertiary_color: int | None

  def format_check(self) -> None:
    format_checker(self.primary_color, "primary_color", 0, 0xffffff)
    format_checker(self.secondary_color,"secondary_color", 0, 0xffffff)
    format_checker(self.tertiary_color, "tertiary_color", 0, 0xffffff)
    return super().format_check()

@dataclass
class UnavailableGuild(Base):
  id: snowflake
  unavailable: bool

@dataclass
class WelcomeScreenChannel(Base):
  channel_id: snowflake
  description: str
  emoji_id: snowflake | None
  emoji_name: str | None

@dataclass
class PromptOption(Base):
  id: snowflake
  channel_ids: list[snowflake]
  role_ids: list[snowflake]
  emoji: emoji_objects.Emoji
  title: str
  description: str | None
  emoji_id: snowflake | Exclude=EXCLUDE
  emoji_name : str | Exclude=EXCLUDE
  emoji_animated: bool | Exclude=EXCLUDE
  
@dataclass
class OnboardingPrompt(Base):
  id: snowflake
  type: Literal[0, 1]
  options: list[PromptOption]
  title: str
  single_select: bool
  required: bool
  in_onboarding: bool

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=FC_PROMPT_TYPE)
    return super().format_check()

@dataclass
class GuildMemberUser(Base):
  id: snowflake

@dataclass
class GuildMember(Base):
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

  name: str | Exclude=EXCLUDE
  afk_timeout: Literal[60, 300, 900, 1800, 3600] | Exclude=EXCLUDE
  system_channel_flags: int | Exclude=EXCLUDE
  features: list[str] | Exclude=EXCLUDE
  premium_progress_bar_enabled: bool | Exclude=EXCLUDE
  region: str | None | Exclude=EXCLUDE
  verification_level: int | None | Exclude=EXCLUDE
  default_message_nontifications: int | None | Exclude=EXCLUDE
  explicit_content_filter: int | None | Exclude=EXCLUDE
  afk_channel_id: snowflake | None | Exclude=EXCLUDE
  icon: image_data | None | Exclude=EXCLUDE
  splash: image_data | None | Exclude=EXCLUDE
  discovery_splash: image_data | None | Exclude=EXCLUDE
  banner: image_data | None | Exclude=EXCLUDE
  system_channel_id: snowflake | None | Exclude=EXCLUDE
  rules_channel_id: snowflake | None | Exclude=EXCLUDE
  public_updates_channel_id: snowflake | None | Exclude=EXCLUDE
  preferred_locale: str | None | Exclude=EXCLUDE
  description: str | None | Exclude=EXCLUDE
  safety_alerts_channel_id: snowflake | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 2, 100)
    format_checker(self.verification_level, "verification_level", in_list=FC_VERIFICATION_LEVEL)
    format_checker(self.default_message_nontifications, "default_message_nontifications", in_list=FC_DEFAULT_MESSAGE_NONTIFICATION_LEVEL)
    format_checker(self.explicit_content_filter, "explicit_content_filter", in_list=FC_EXPLICIT_CONTENT_FILTER_LEVEL)
    format_checker(self.afk_timeout, "afk_timeout", in_list=FC_AFK_TIMEOUT)
    format_checker(self.preferred_locale, "preferred_locale", in_list=list(locales.LOCALES.keys()))
    format_checker(self.description, "description", 0, 300)
    return super().format_check()

@dataclass
class GetGuildChannels(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildChannel(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "post"

  name: str
  type: int | None | Exclude=EXCLUDE
  topic: str | None | Exclude=EXCLUDE
  bitrate: int | None | Exclude=EXCLUDE
  user_limit: int | None | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE
  position: int | None | Exclude=EXCLUDE
  permission_overwrite: list[b_channel.Overwrite] | None | Exclude=EXCLUDE
  parent_id: snowflake | None | Exclude=EXCLUDE
  nsfw: bool | None | Exclude=EXCLUDE
  rtc_region: str | None | Exclude=EXCLUDE
  video_quality_mode: int | None | Exclude=EXCLUDE
  default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None | Exclude=EXCLUDE
  default_reaction_emoji: b_channel.DefaultReaction | None | Exclude=EXCLUDE
  available_tags: list[b_channel.ForumTag] | None | Exclude=EXCLUDE
  default_sort_order: int | None | Exclude=EXCLUDE
  default_forum_layout: int | None | Exclude=EXCLUDE
  default_thread_rate_limit_per_user: int | None | Exclude=EXCLUDE
  flags: int | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    def __gen_str(select_list: list):
      return f"cannot be used unless `type` is one of {str(select_list)}"
    def __check_in_list(value, value_name: str, in_list: list):
      if not isinstance(value, Exclude) and value not in in_list:
        raise PayloadFormatError(value_name, __gen_str(in_list))
    # channel type check
    __check_in_list(self.topic, "topic", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_ANNOUNCEMENT, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.bitrate, "bitrate", [b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_STAGE_VOICE])
    __check_in_list(self.user_limit, "user_limit", [b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_STAGE_VOICE])
    __check_in_list(self.rate_limit_per_user, "rate_limit_per_user", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_STAGE_VOICE, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.parent_id, "parent_id", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_ANNOUNCEMENT, b_channel.CT_GUILD_STAGE_VOICE, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.rtc_region, "rtc_region", [b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_STAGE_VOICE])
    __check_in_list(self.video_quality_mode, "video_quality_mode", [b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_STAGE_VOICE])
    __check_in_list(self.default_auto_archive_duration, "default_auto_archive_duration", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_ANNOUNCEMENT, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.default_reaction_emoji, "default_reaction_emoji", [b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.available_tags, "available_tags", [b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.default_sort_order, "default_sort_order", [b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.default_forum_layout, "default_forum_layout", [b_channel.CT_GUILD_FORUM])
    __check_in_list(self.default_thread_rate_limit_per_user, "default_thread_rate_limit_per_user", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_ANNOUNCEMENT, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    __check_in_list(self.flags, "flags", [b_channel.CT_GUILD_TEXT, b_channel.CT_GUILD_VOICE, b_channel.CT_GUILD_ANNOUNCEMENT, b_channel.CT_GUILD_FORUM, b_channel.CT_GUILD_MEDIA])
    # format check
    format_checker(self.name, "name", 1, 100)
    format_checker(self.type, "type", in_list=b_channel.FC_CHANNEL_TYPE)
    format_checker(self.topic, "topic", 0, 1024)
    if self.type == b_channel.CT_GUILD_STAGE_VOICE:
      format_checker(self.bitrate, "bitrate", 8000, 64000)
    else:
      format_checker(self.bitrate, "bitrate", 8000, 384000)
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    format_checker(self.video_quality_mode, "video_quality_mode", in_list=b_channel.FC_VIDEO_QUALITY_MODE)
    format_checker(self.default_auto_archive_duration, "default_auto_archive_duration", in_list=b_channel.FC_AUTO_ARCHIVE_DURATION)
    format_checker(self.default_sort_order, "default_sort_order", in_list=FC_SORT_ORDER_TYPE)
    format_checker(self.default_forum_layout, "default_forum_layout", in_list=FC_FORUM_LAYOUT_TYPES)
    format_checker(self.default_thread_rate_limit_per_user, "default_thread_rate_limit_per_user", 0, 21600)
    return super().format_check()

@dataclass
class ModifyGuildChannelPositions(__GuildBase):
  req_url:  ClassVar[str] = "/channels"
  req_type: ClassVar[str] = "patch"

  id: snowflake
  position: int | None | Exclude=EXCLUDE
  lock_permissions: bool | None | Exclude=EXCLUDE
  parent_id: snowflake | None | Exclude=EXCLUDE
  flags: int | None | Exclude=EXCLUDE

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

  nick: str | None | Exclude=EXCLUDE
  roles: list[snowflake] | None | Exclude=EXCLUDE
  mute: bool | None | Exclude=EXCLUDE
  deaf: bool | None | Exclude=EXCLUDE
  channel_id: snowflake | None | Exclude=EXCLUDE
  communication_disabled_until: ISO8601timestamp | None | Exclude=EXCLUDE
  flags: int | None | Exclude=EXCLUDE

@dataclass
class ModifyCurrentMember(__GuildBase):
  req_url:  ClassVar[str] = "/members/@me"
  req_type: ClassVar[str] = "patch"

  nick: str | None | Exclude=EXCLUDE
  banner: image_data | None | Exclude=EXCLUDE
  avatar: image_data | None | Exclude=EXCLUDE
  bio: str | None | Exclude=EXCLUDE

@dataclass
class ModifyCurrentUserNick(__GuildBase):
  req_url:  ClassVar[str] = "/members/@me/nick"
  req_type: ClassVar[str] = "patch"

  nick: str | None | Exclude=EXCLUDE

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

  delete_message_seconds: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.delete_message_seconds, "delete_message_seconds", 0, 604800)
    return super().format_check()

@dataclass
class RemoveGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bans/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkGuildBan(__GuildBase):
  req_url:  ClassVar[str] = "/bulk-ban"
  req_type: ClassVar[str] = "post"

  user_ids: list[snowflake]
  delete_message_seconds: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.user_ids, "user_ids", 0, 200)
    format_checker(self.delete_message_seconds, "delete_message_seconds", 0, 604800)
    return super().format_check()

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

  def format_check(self) -> None:
    format_checker(self.name, "name", 0, 100)
    format_checker(self.color, "color", 0, 0xffffff)
    return super().format_check()

@dataclass
class ModifyGuildRolePositions(__GuildBase):
  req_url:  ClassVar[str] = "/roles"
  req_type: ClassVar[str] = "patch"

  id: snowflake
  position: int | None | Exclude=EXCLUDE

@dataclass
class ModifyGuildRole(__GuildBase):
  req_url:  ClassVar[str] = "/roles/<role.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  permissions: str | Exclude=EXCLUDE
  color: int | Exclude=EXCLUDE
  colors: RoleColors | Exclude=EXCLUDE
  hoist: bool | Exclude=EXCLUDE
  icon: image_data | Exclude=EXCLUDE
  unicode_emoji: str | Exclude=EXCLUDE
  mentionable: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 0, 100)
    format_checker(self.color, "color", 0, 0xffffff)
    return super().format_check()

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
  reason: str | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.days, "days", 1, 30)
    return super().format_check()

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

  enabled: bool
  channel_id: snowflake | None

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

  def format_check(self) -> None:
    format_checker(self.welcome_channels, "welcome_channels", 0, 5)
    return super().format_check()

@dataclass
class GetGuildOnboarding(__GuildBase):
  req_url:  ClassVar[str] = "/onboarding"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildOnboarding(__GuildBase):
  req_url:  ClassVar[str] = "/onboarding"
  req_type: ClassVar[str] = "put"

  prompts: list[OnboardingPrompt] | Exclude=EXCLUDE
  default_channel_ids: list[snowflake] | Exclude=EXCLUDE
  enabled: bool | Exclude=EXCLUDE
  mode: Literal[0, 1] | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.mode, "mode", in_list=FC_ONBOARDING_MODE)
    return super().format_check()

@dataclass
class ModifyGuildIncidentActions(__GuildBase):
  req_url:  ClassVar[str] = "/incident-actions"
  req_type: ClassVar[str] = "put"

  invites_disabled_until: ISO8601timestamp | None | Exclude=EXCLUDE
  dms_disabled_until: ISO8601timestamp | None | Exclude=EXCLUDE