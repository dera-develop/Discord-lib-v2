from dataclasses import dataclass
from typing import Literal, BinaryIO, ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude
from discord_lib2.objects.http_request.base.body_base import FormFile

from discord_lib2.objects.http_request.base import b_message
from discord_lib2.objects.other import component

base64icon = str
snowflake  = str
ISO8601timestamp = str

@dataclass
class __ChannelBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels"

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

@dataclass
class DefaultReaction:
  emoji_id: snowflake
  emoji_name: str

@dataclass
class ForumTag:
  id: snowflake
  name: str
  moderated: bool
  emoji_id: snowflake
  emoji_name: str

@dataclass
class Overwrite:
  id: snowflake
  type: int
  allow: str
  deny: str

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

  def format_check(self, filtered_dict) -> None:
    if not 1 <=len(filtered_dict.get("name")) <= 100:
      raise body_base.PayloadFormatError("'name': The character count must be between 1 and 100.")

@dataclass
class ModifyChannelGuildChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  name: str
  type: int
  position: int | None
  topic: str | None
  nsfw: bool | None
  rate_limit_per_user: int | None
  bitrate: int | None
  user_limit: int | None
  permission_overwrites: list[Overwrite] | None
  parent_id: snowflake | None
  rtc_region: str | None | None
  voice_quality_mode: int | None
  default_auto_archive_duration: int | None
  flags: int
  available_tags: list[ForumTag]
  default_reaction_emoji: DefaultReaction | None
  default_thread_rate_limit_per_user: int
  default_sort_order: int | None
  default_forum_layout: int

@dataclass
class ModifyChannelThread(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  name: str
  archived: bool
  auto_archive_duration: int
  locked: bool
  invitable: bool
  flags: int
  rate_limit_per_user: int | None
  applied_tags: list[snowflake] | None

@dataclass
class SetVoiceChannelStatus(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/voice-status"
  req_type: ClassVar[str] = "put"

  status: str | None

@dataclass
class DeleteCloseChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class EditChannelPermissions(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/permissions/<overwrite.id>"
  req_type: ClassVar[str] = "put"

  type: int
  allow: str | None | Exclude = Exclude()
  deny: str | None | Exclude = Exclude()

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
  target_user_id: snowflake
  target_application_id: snowflake

  target_users_file: BinaryIO | Exclude = Exclude()
  payload_json: str | Exclude = Exclude()
  role_ids: list[snowflake] | Exclude = Exclude()

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
  auto_archive_duration: int | Exclude = Exclude()
  rate_limit_per_user: int | None | Exclude = Exclude()

@dataclass
class StartThreadwithoutMessage(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads"
  req_type: ClassVar[str] = "post"

  name: str
  auto_archive_duration: Literal[60, 1440, 4320, 10080] | Exclude = Exclude()
  type: int | Exclude = Exclude()
  invitable: bool | Exclude = Exclude()
  rate_limit_per_user: int | None | Exclude = Exclude()

@dataclass
class StartThreadinForumorMediaChannel(__ChannelBase):
  req_url:  ClassVar[str] = "/<channel.id>/threads"
  req_type: ClassVar[str] = "post"

  @dataclass
  class ForumandMediaThreadMessageParams:
    content: str | Exclude = Exclude()
    embeds: list[b_message.Embed] | Exclude = Exclude()
    allowed_mentions: b_message.AllowedMentions | Exclude = Exclude()
    components: list[component.ComponentClass] | Exclude = Exclude()
    sticker_ids: list[snowflake] | Exclude = Exclude()
    attachments: list[b_message.AttachmentRequest] | Exclude = Exclude()
    flags: int | Exclude = Exclude()

  name: str
  message: ForumandMediaThreadMessageParams
  auto_archive_duration: int | Exclude = Exclude()
  rate_limit_per_user: int | None | Exclude = Exclude()
  applied_tags: list[snowflake] | Exclude = Exclude()
  files: FormFile = FormFile()
  payload_json: str | Exclude = Exclude()

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