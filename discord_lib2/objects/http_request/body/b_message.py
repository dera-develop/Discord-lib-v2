from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude
from discord_lib2.objects.http_request.body.body_base import FormFile

from discord_lib2.objects.other import component

snowflake = str
ISO8601timestamp = str

@dataclass
class __MessageBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels/<channel.id>"

F_CROSSPOSTED = 1 << 0
F_IS_CROSSPOST = 1 << 1
F_SUPPRESS_EMBEDS = 1 << 2
F_SOURCE_MESSAGE_DELETED = 1 << 3
F_URGENT = 1 << 4
F_HAS_THREAD = 1 << 5
F_EPHEMERAL = 1 << 6
F_LOADING = 1 << 7
F_FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
F_SUPPRESS_NOTIFICATIONS = 1 << 12
F_IS_VOICE_MESSAGE = 1 << 13
F_HAS_SNAPSHOT = 1 << 14
F_IS_COMPONENTS_V2 = 1 << 15

@dataclass
class Embed(__MessageBase):
  ET_RICH: ClassVar[str] = "rich"
  ET_IMAGE: ClassVar[str] = "image"
  ET_VIDEO: ClassVar[str] = "video"
  ET_GIFV: ClassVar[str] = "gifv"
  ET_ARTICLE: ClassVar[str] = "article"
  ET_LINK: ClassVar[str] = "link"

  MF_IS_ANIMATED: ClassVar[int] = 1 << 5

  class ET_PollResultEmbed:
    POLL_QUESTION_TEXT: ClassVar[str] = "poll_question_text"
    VICTOR_ANSWER_VOTES: ClassVar[str] = "victor_answer_votes"
    TOTAL_VOTES: ClassVar[str] = "total_votes"
    VICTOR_ANSWER_ID: ClassVar[str] = "victor_answer_id"
    VICTOR_ANSWER_TEXT: ClassVar[str] = "victor_answer_text"
    VICTOR_ANSWER_EMOJI_ID: ClassVar[str] = "victor_answer_emoji_id"
    VICTOR_ANSWER_EMOJI_NAME: ClassVar[str] = "victor_answer_emoji_name"
    VICTOR_ANSWER_EMOJI_ANIMATED: ClassVar[str] = "victor_answer_emoji_animated"

  @dataclass
  class Footer:
    text: str
    icon_url: str | Exclude = Exclude()
    proxy_icon_url: str | Exclude = Exclude()

  @dataclass
  class Image:
    url: str
    proxy_url: str | Exclude = Exclude()
    height: int | Exclude = Exclude()
    width: int | Exclude = Exclude()
    content_type: str | Exclude = Exclude()
    placeholder: str | Exclude = Exclude()
    placeholder_version: int | Exclude = Exclude()
    description: str | Exclude = Exclude()
    flags: int | Exclude = Exclude()

  @dataclass
  class Video:
    url: str | Exclude = Exclude()
    proxy_url: str | Exclude = Exclude()
    height: int | Exclude = Exclude()
    width: int | Exclude = Exclude()
    content_type: str | Exclude = Exclude()
    placeholder: str | Exclude = Exclude()
    placeholder_version: int | Exclude = Exclude()
    description: str | Exclude = Exclude()
    flags: int | Exclude = Exclude()

  @dataclass
  class Provider:
    name: str | Exclude = Exclude()
    url: str | Exclude = Exclude()

  @dataclass
  class Author:
    name: str
    url: str | Exclude = Exclude()
    icon_url: str | Exclude = Exclude()
    proxy_icon_url: str | Exclude = Exclude()

  @dataclass
  class Field:
    name: str
    value: str
    inline: bool | Exclude = Exclude()

  title: str | Exclude = Exclude()
  type: str | Exclude = Exclude()
  description: str | Exclude = Exclude()
  url: str | Exclude = Exclude()
  timestamp: ISO8601timestamp | Exclude = Exclude()
  color: int | Exclude = Exclude()
  footer: Footer | Exclude = Exclude()
  image: Image | Exclude = Exclude()
  thumbnail: Image | Exclude = Exclude()
  video: Video | Exclude = Exclude()
  provider: Provider | Exclude = Exclude()
  author: Author | Exclude = Exclude()
  fields: list[Field] | Exclude = Exclude()
  flags: int | Exclude = Exclude()

@dataclass
class AllowedMentions:
  T_ROLE_MENTION: ClassVar[str] = "roles"
  T_USER_MENTIONS: ClassVar[str] = "users"
  T_EVERYONE_MENTIONS: ClassVar[str] = "everyone"

  parse: list[str] | Exclude = Exclude()
  roles: list[snowflake] | Exclude = Exclude()
  users: list[snowflake] | Exclude = Exclude()
  replied_user: bool | Exclude = Exclude()

@dataclass
class MessageReference:
  T_DEFAULT: ClassVar[int] = 0
  T_FORWARD: ClassVar[int] = 1

  type: int | Exclude = Exclude()
  message_id: snowflake | Exclude = Exclude()
  channel_id: snowflake | Exclude = Exclude()
  guild_id: snowflake | Exclude = Exclude()
  fail_if_not_exists: bool | Exclude = Exclude()

@dataclass
class AttachmentRequest:
  id: snowflake | int
  filename: str | Exclude = Exclude()
  title: str | Exclude = Exclude()
  description: str | Exclude = Exclude()
  duration_secs: float | Exclude = Exclude()
  waveform: str | Exclude = Exclude()
  is_spoiler: bool | Exclude = Exclude()

@dataclass
class ShardClientTheme:
  BT_UNSET: ClassVar[int] = 0
  BT_DARK: ClassVar[int] = 1
  BT_LIGHT: ClassVar[int] = 2
  BT_DARKER: ClassVar[int] = 3
  BT_MIDNIGHT: ClassVar[int] = 4

  colors: list[str]
  gradient_angle: int
  base_mix: int
  base_theme: int | Exclude = Exclude()

@dataclass
class GetChannelMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages"
  req_type: ClassVar[str] = "get"

@dataclass
class SearchGuildMessages(body_base.BaseClass):
  req_url:  ClassVar[str] = "/guilds/<guild.id>/messages/search"
  req_type: ClassVar[str] = "get"

@dataclass
class GetChannelMessage_MessageID(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages"
  req_type: ClassVar[str] = "post"

  content: str | Exclude = Exclude()
  nonce: int | str | Exclude = Exclude()
  tts: bool | Exclude = Exclude()
  embeds: list[Embed] | Exclude = Exclude()
  allowed_mentions: AllowedMentions | Exclude = Exclude()
  message_reference: MessageReference | Exclude = Exclude()
  components: list[component.ComponentClass] | Exclude = Exclude()
  sticker_ids: list[snowflake] | Exclude = Exclude()
  files: FormFile = FormFile()
  payload_json: str | Exclude = Exclude()
  attachments: list[AttachmentRequest] | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  enforce_nonce: bool | Exclude = Exclude()
  poll: ShardClientTheme | Exclude = Exclude()

@dataclass
class CrosspostMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/crosspost"
  req_type: ClassVar[str] = "post"

@dataclass
class CreateReaction(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions/<emoji.id>/@me"
  req_type: ClassVar[str] = "put"

@dataclass
class DeleteOwnReaction(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions/<emoji.id>/@me"
  req_type: ClassVar[str] = "delete"

@dataclass
class DeleteUserReaction(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions/<emoji.id>/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetReactions(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions/<emoji.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class DeleteAllReactions(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions"
  req_type: ClassVar[str] = "delete"

@dataclass
class DeleteAllReactionsforEmoji(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>/reactions/<emoji.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class EditMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>"
  req_type: ClassVar[str] = "patch"

  content: str | None | Exclude = Exclude()
  embeds: list[Embed] | None | Exclude = Exclude()
  flags: int | None | Exclude = Exclude()
  allowed_mentions: AllowedMentions | None | Exclude = Exclude()
  components: list[component.ComponentClass] | None | Exclude = Exclude()
  files: FormFile = FormFile()
  payload_json: str | None | Exclude = Exclude()
  attachments: list[AttachmentRequest] | None | Exclude = Exclude()

@dataclass
class DeleteMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkDeleteMessages(__MessageBase):
  req_url:  ClassVar[str] = "/messages/bulk-delete"
  req_type: ClassVar[str] = "post"

  messages: list[snowflake]

@dataclass
class GetChannelPins(__MessageBase):
  req_url:  ClassVar[str] = "/messages/pins"
  req_type: ClassVar[str] = "get"

@dataclass
class PinMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/pins/<message.id>"
  req_type: ClassVar[str] = "put"

@dataclass
class UnpinMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/pins/<message.id>"
  req_type: ClassVar[str] = "delete"