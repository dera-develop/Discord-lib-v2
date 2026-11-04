from dataclasses import dataclass, field
from typing import Literal, BinaryIO, ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, FormFile, Base

from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.http_request.body import b_user
from discord_lib2.objects.other import component

from discord_lib2.objects.http_request.format_checker import format_checker, PayloadFormatError

base64icon = str
snowflake  = str
ISO8601timestamp = str
EXCLUDE = Exclude()

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

VQM_AUTO = 1
VQM_FULL = 2

CF_PINNED = 1 << 1
CF_REQUIRE_TAG = 1 << 4
CF_HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15

SOT_CATEST_ACTIVITY = 0
SOT_CREATION_DATE = 1

FLT_NOT_SET = 0
FLT_LIST_VIEW = 1
FLT_GALLERY_VIEW = 2

# format check
FC_CHANNEL_TYPE = (
  CT_GUILD_TEXT, CT_DM, CT_GUILD_VOICE, CT_GROUP_DM, CT_GUILD_CATEGORY, CT_GUILD_ANNOUNCEMENT, CT_ANNOUNCEMENT_THREAD,
  CT_PUBLIC_THREAD, CT_PRIVATE_THREAD, CT_GUILD_STAGE_VOICE, CT_GUILD_DIRECTORY, CT_GUILD_FORUM, CT_GUILD_MEDIA
)
FC_VIDEO_QUALITY_MODE = (VQM_AUTO, VQM_FULL)
FC_SORT_ORDER_TYPE = (SOT_CATEST_ACTIVITY, SOT_CREATION_DATE)
FC_FORUM_LAYOUT_TYPE = (FLT_NOT_SET, FLT_LIST_VIEW, FLT_GALLERY_VIEW)
FC_AUTO_ARCHIVE_DURATION = (60, 1440, 4320, 10080)
FC_INVITE_TARGET_TYPE = (1, 2)

@dataclass
class __ChannelBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels"

@dataclass
class Overwrite(Base):
  id: snowflake
  type: int
  allow: str
  deny: str

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=[0, 1])
    return super().format_check()

@dataclass
class ThreadMetadata(Base):
  archived: bool
  auto_archive_duration: Literal[60, 1440, 4320, 10080]
  archive_timestamp: ISO8601timestamp
  locked: bool
  invitable: bool | Exclude=EXCLUDE
  create_timestamp: ISO8601timestamp | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.auto_archive_duration, "auto_archive_duration", in_list=FC_AUTO_ARCHIVE_DURATION)
    return super().format_check()

@dataclass
class GuildMember(Base):
  id: snowflake

@dataclass
class ThreadMember(Base):
  join_timestamp: ISO8601timestamp
  flags: int
  id: snowflake | Exclude=EXCLUDE
  user_id: snowflake | Exclude=EXCLUDE
  member: GuildMember | Exclude=EXCLUDE

@dataclass
class DefaultReaction(Base):
  emoji_id: snowflake | None
  emoji_name: str | None

@dataclass
class ForumTag(Base):
  id: snowflake
  name: str
  moderated: bool
  emoji_id: snowflake | None
  emoji_name: str | None

  def format_check(self) -> None:
    format_checker(self.name, "name", 0, 20)
    return super().format_check()

@dataclass
class Channel(Base):
  id: snowflake
  type: int
  rate_limit_per_user: int
  message_count: int
  guild_id: snowflake | Exclude=EXCLUDE
  position: int | Exclude=EXCLUDE
  permission_overwrites: list[Overwrite] | Exclude=EXCLUDE
  name: str | None | Exclude=EXCLUDE
  topic: str | None | Exclude=EXCLUDE
  nsfw: bool | Exclude=EXCLUDE
  last_message_id: snowflake | None | Exclude=EXCLUDE
  bitrate: int | Exclude=EXCLUDE
  user_limit: int | Exclude=EXCLUDE
  recipients: list[b_user.User] | Exclude=EXCLUDE
  icon: str | None | Exclude=EXCLUDE
  owner_id: snowflake | Exclude=EXCLUDE
  application_id: snowflake | None | Exclude=EXCLUDE
  managed: bool | Exclude=EXCLUDE
  parent_id: snowflake | None | Exclude=EXCLUDE
  last_pin_timestamp: ISO8601timestamp | None | Exclude=EXCLUDE
  rtc_region: str | None | Exclude=EXCLUDE
  video_quality_mode: int | Exclude=EXCLUDE
  member_count: int | Exclude=EXCLUDE
  thread_metadata: ThreadMetadata | Exclude=EXCLUDE
  member: ThreadMember | Exclude=EXCLUDE
  default_auto_archive_duration: int | Exclude=EXCLUDE
  permissions: str | Exclude=EXCLUDE
  app_permissions: str | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  total_message_sent: int | Exclude=EXCLUDE
  available_tags: list[ForumTag] | Exclude=EXCLUDE
  applied_tags: list[snowflake] | Exclude=EXCLUDE
  default_reaction_emoji: DefaultReaction | None | Exclude=EXCLUDE
  default_thread_rate_limit_per_user: int | Exclude=EXCLUDE
  default_sort_order: int | None | Exclude=EXCLUDE
  default_forum_layout: int | Exclude=EXCLUDE

@dataclass
class ForumandMediaThreadMessageParams:
  content: str | Exclude=EXCLUDE
  embeds: list[b_message.Embed] | Exclude=EXCLUDE
  allowed_mentions: b_message.AllowedMentions | Exclude=EXCLUDE
  components: list[component.ComponentClass] | Exclude=EXCLUDE
  sticker_ids: list[snowflake] | Exclude=EXCLUDE
  attachments: list[b_message.AttachmentRequest] | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE

@dataclass
class GetChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyChannelGroupDM(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  name: str
  icon: base64icon

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    return super().format_check()

@dataclass
class ModifyChannelGuildChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  type: int | Exclude=EXCLUDE
  position: int | None | Exclude=EXCLUDE
  topic: str | None | Exclude=EXCLUDE
  nsfw: bool | None | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE
  bitrate: int | None | Exclude=EXCLUDE
  user_limit: int | None | Exclude=EXCLUDE
  permission_overwrites: list[Overwrite] | None | Exclude=EXCLUDE
  parent_id: snowflake | None | Exclude=EXCLUDE
  rtc_region: str | None | None | Exclude=EXCLUDE
  video_quality_mode: int | None | Exclude=EXCLUDE
  default_auto_archive_duration: int | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  available_tags: list[ForumTag] | Exclude=EXCLUDE
  default_reaction_emoji: DefaultReaction | None | Exclude=EXCLUDE
  default_thread_rate_limit_per_user: int | Exclude=EXCLUDE
  default_sort_order: int | None | Exclude=EXCLUDE
  default_forum_layout: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    def __gen_str(select_list: list):
      return f"cannot be used unless `type` is one of {str(select_list)}"
    def __check_in_list(value, value_name: str, in_list: list):
      if not isinstance(value, Exclude) and value not in in_list:
        raise PayloadFormatError(value_name, __gen_str(in_list))
    # channel type check
    __check_in_list(self.topic, "topic", [CT_GUILD_TEXT, CT_GUILD_ANNOUNCEMENT, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.nsfw, "nsfw", [CT_GUILD_TEXT, CT_GUILD_VOICE, CT_GUILD_ANNOUNCEMENT, CT_GUILD_STAGE_VOICE, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.rate_limit_per_user, "rate_limit_per_user", [CT_GUILD_TEXT, CT_GUILD_VOICE, CT_GUILD_STAGE_VOICE, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.bitrate, "bitrate", [CT_GUILD_VOICE, CT_GUILD_STAGE_VOICE])
    __check_in_list(self.user_limit, "user_limit", [CT_GUILD_VOICE, CT_GUILD_STAGE_VOICE])
    __check_in_list(self.parent_id, "parent_id", [CT_GUILD_TEXT, CT_GUILD_VOICE, CT_GUILD_ANNOUNCEMENT, CT_GUILD_STAGE_VOICE, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.rtc_region, "rtc_region", [CT_GUILD_VOICE, CT_GUILD_STAGE_VOICE])
    __check_in_list(self.video_quality_mode, "video_quality_mode", [CT_GUILD_VOICE, CT_GUILD_STAGE_VOICE])
    __check_in_list(self.default_auto_archive_duration, "default_auto_archive_duration", [CT_GUILD_TEXT, CT_GUILD_ANNOUNCEMENT, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.flags, "flags", [CT_GUILD_TEXT, CT_GUILD_VOICE, CT_GUILD_ANNOUNCEMENT, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.available_tags, "available_tags", [CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.default_reaction_emoji, "default_reaction_emoji", [CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.default_thread_rate_limit_per_user, "default_thread_rate_limit_per_user", [CT_GUILD_TEXT, CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.default_sort_order, "default_sort_order", [CT_GUILD_FORUM, CT_GUILD_MEDIA])
    __check_in_list(self.default_forum_layout, "default_forum_layout", [CT_GUILD_FORUM])
    # format check
    format_checker(self.name, "name", 1, 100)
    format_checker(self.type, "type", in_list=(CT_GUILD_TEXT, CT_GUILD_ANNOUNCEMENT))
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    format_checker(self.bitrate, "bitrate", 8000, 384000)
    format_checker(self.video_quality_mode, "video_quality_mode", in_list=FC_VIDEO_QUALITY_MODE)
    format_checker(self.available_tags, "available_tags", 0, 20)
    format_checker(self.default_thread_rate_limit_per_user, "default_thread_rate_limit_per_user", 0, 21600)
    format_checker(self.default_sort_order, "default_sort_order", in_list=FC_SORT_ORDER_TYPE)
    format_checker(self.default_forum_layout, "default_forum_layout", in_list=FC_FORUM_LAYOUT_TYPE)
    if self.type in [CT_GUILD_FORUM, CT_GUILD_MEDIA]: format_checker(self.topic, "topic", 0, 4096)
    else:                                             format_checker(self.topic, "topic", 0, 1024)
    if self.type == CT_GUILD_VOICE: format_checker(self.user_limit, "user_limit", 0, 99)
    else:                           format_checker(self.user_limit, "user_limit", 0, 10000)
    return super().format_check()

@dataclass
class ModifyChannelThread(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  archived: bool | Exclude=EXCLUDE
  auto_archive_duration: Literal[60, 1440, 4320, 10080] | Exclude=EXCLUDE
  locked: bool | Exclude=EXCLUDE
  invitable: bool | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE
  applied_tags: list[snowflake] | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.auto_archive_duration, "auto_archive_duration", in_list=FC_AUTO_ARCHIVE_DURATION)
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    format_checker(self.applied_tags, "applied_tags", 0, 5)
    return super().format_check()

@dataclass
class SetVoiceChannelStatus(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/voice-status"
  req_type: ClassVar[str] = "put"

  status: str | None

  def format_check(self) -> None:
    format_checker(self.status, "status", 0, 500)
    return super().format_check()

@dataclass
class DeleteCloseChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class EditChannelPermissions(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/permissions/<overwrite.id>"
  req_type: ClassVar[str] = "put"

  type: int
  allow: str | None | Exclude=EXCLUDE
  deny: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=[0, 1])
    return super().format_check()

@dataclass
class GetChannelInvites(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/invites"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateChannelInvite(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/invites"
  req_type: ClassVar[str] = "post"

  max_age: int
  max_users: int
  temporary: bool
  unique: bool
  target_type: int
  target_user_id: snowflake | Exclude=EXCLUDE
  target_application_id: snowflake | Exclude=EXCLUDE
  target_users_file: BinaryIO | Exclude=EXCLUDE
  target_user_ids: list[snowflake] | Exclude=EXCLUDE
  payload_json: str | Exclude=EXCLUDE
  role_ids: list[snowflake] | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.max_age, "max_age", 0, 604800)
    format_checker(self.max_users, "max_users", 0, 100)
    format_checker(self.target_type, "target_type", in_list=FC_INVITE_TARGET_TYPE)
    format_checker(self.target_user_ids, "target_user_ids", 0, 1000)
    if self.target_type == 1 and isinstance(self.target_user_id, Exclude):
      raise PayloadFormatError("target_type", "required this argument if target_type is 1")
    if self.target_type == 2 and isinstance(self.target_application_id, Exclude):
      raise PayloadFormatError("target_type", "required this argument if target_type is 2")
    return super().format_check()

@dataclass
class DeleteChannelPermission(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/permissions/<overwrite.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class FollowAnnouncementChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/followers"
  req_type: ClassVar[str] = "post"

  webhook_channel_id: snowflake

@dataclass
class TriggerTypingIndicator(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/typing"
  req_type: ClassVar[str] = "post"

@dataclass
class GroupDMAddRecipient(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/recipients/<user.id>"
  req_type: ClassVar[str] = "put"

  access_token: str
  nick: str

@dataclass
class GroupDMRemoveRecipient(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/recipients/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class StartThreadfromMessage(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/messages/<message.id>"
  req_type: ClassVar[str] = "post"

  name: str
  auto_archive_duration: Literal[60, 1440, 4320, 10080] | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.auto_archive_duration, "auto_archive_duration", in_list=FC_AUTO_ARCHIVE_DURATION)
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    return super().format_check()

@dataclass
class StartThreadwithoutMessage(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads"
  req_type: ClassVar[str] = "post"

  name: str
  auto_archive_duration: Literal[60, 1440, 4320, 10080] | Exclude=EXCLUDE
  type: int | Exclude=EXCLUDE
  invitable: bool | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.auto_archive_duration, "auto_archive_duration", in_list=FC_AUTO_ARCHIVE_DURATION)
    format_checker(self.type, "type", in_list=[CT_PUBLIC_THREAD, CT_PRIVATE_THREAD, CT_ANNOUNCEMENT_THREAD])
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    return super().format_check()

@dataclass
class StartThreadinForumorMediaChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads"
  req_type: ClassVar[str] = "post"

  name: str
  message: ForumandMediaThreadMessageParams
  auto_archive_duration: int | Exclude=EXCLUDE
  rate_limit_per_user: int | None | Exclude=EXCLUDE
  applied_tags: list[snowflake] | Exclude=EXCLUDE
  files: FormFile = field(default_factory=FormFile)
  payload_json: str | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.auto_archive_duration, "auto_archive_duration", in_list=FC_AUTO_ARCHIVE_DURATION)
    format_checker(self.rate_limit_per_user, "rate_limit_per_user", 0, 21600)
    return super().format_check()

@dataclass
class JoinThread(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members/@me"
  req_type: ClassVar[str] = "put"

@dataclass
class AddThreadMember(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members/<user.id>"
  req_type: ClassVar[str] = "put"

@dataclass
class LeaveThread(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members/@me"
  req_type: ClassVar[str] = "delete"

@dataclass
class RemoveThreadMember(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetThreadMember(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members/<user.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ListThreadMembers(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/thread-members"
  req_type: ClassVar[str] = "get"

@dataclass
class ListPublicArchivedThreads(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads/archived/public"
  req_type: ClassVar[str] = "get"

@dataclass
class ListPrivateArchivedThreads(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads/archived/private"
  req_type: ClassVar[str] = "get"

@dataclass
class ListJoinedPrivateArchivedThreads(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/users/@me/threads/archived/private"
  req_type: ClassVar[str] = "get"