from dataclasses import dataclass, field
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, FormFile, Base

from discord_lib2.objects.http_request.body import b_poll
from discord_lib2.objects.other import component

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
ISO8601timestamp = str
EXCLUDE = Exclude()

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
class __MessageBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels/<channel.id>"

@dataclass
class Embed(__MessageBase):
  ET_RICH: ClassVar[str] = "rich"
  ET_IMAGE: ClassVar[str] = "image"
  ET_VIDEO: ClassVar[str] = "video"
  ET_GIFV: ClassVar[str] = "gifv"
  ET_ARTICLE: ClassVar[str] = "article"
  ET_LINK: ClassVar[str] = "link"

  __FC_EMBED_TYPE: ClassVar[tuple] = (ET_RICH, ET_IMAGE, ET_VIDEO, ET_GIFV, ET_ARTICLE, ET_LINK)

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
  class Footer(Base):
    text: str
    icon_url: str | Exclude=EXCLUDE
    proxy_icon_url: str | Exclude=EXCLUDE

    def format_check(self) -> None:
      format_checker(self.text, "text", 0, 2048)
      return super().format_check()

  @dataclass
  class Image(Base):
    url: str
    proxy_url: str | Exclude=EXCLUDE
    height: int | Exclude=EXCLUDE
    width: int | Exclude=EXCLUDE
    content_type: str | Exclude=EXCLUDE
    placeholder: str | Exclude=EXCLUDE
    placeholder_version: int | Exclude=EXCLUDE
    description: str | Exclude=EXCLUDE
    flags: int | Exclude=EXCLUDE

  @dataclass
  class Video(Base):
    url: str | Exclude=EXCLUDE
    proxy_url: str | Exclude=EXCLUDE
    height: int | Exclude=EXCLUDE
    width: int | Exclude=EXCLUDE
    content_type: str | Exclude=EXCLUDE
    placeholder: str | Exclude=EXCLUDE
    placeholder_version: int | Exclude=EXCLUDE
    description: str | Exclude=EXCLUDE
    flags: int | Exclude=EXCLUDE

  @dataclass
  class Provider(Base):
    name: str | Exclude=EXCLUDE
    url: str | Exclude=EXCLUDE

  @dataclass
  class Author(Base):
    name: str
    url: str | Exclude=EXCLUDE
    icon_url: str | Exclude=EXCLUDE
    proxy_icon_url: str | Exclude=EXCLUDE

    def format_check(self) -> None:
      format_checker(self.name, "name", 0, 256)
      return super().format_check()

  @dataclass
  class Field(Base):
    name: str
    value: str
    inline: bool | Exclude=EXCLUDE

    def format_check(self) -> None:
      format_checker(self.name, "name", 0, 256)
      format_checker(self.value, "value", 0, 1024)
      return super().format_check()

  title: str | Exclude=EXCLUDE
  type: str | Exclude=EXCLUDE
  description: str | Exclude=EXCLUDE
  url: str | Exclude=EXCLUDE
  timestamp: ISO8601timestamp | Exclude=EXCLUDE
  color: int | Exclude=EXCLUDE
  footer: Footer | Exclude=EXCLUDE
  image: Image | Exclude=EXCLUDE
  thumbnail: Image | Exclude=EXCLUDE
  video: Video | Exclude=EXCLUDE
  provider: Provider | Exclude=EXCLUDE
  author: Author | Exclude=EXCLUDE
  fields: list[Field] | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.title, "title", 0, 256)
    format_checker(self.type, "type", in_list=self.__FC_EMBED_TYPE)
    format_checker(self.description, "description", 0, 4096)
    format_checker(self.fields, "fields", 0, 25)
    return super().format_check()

@dataclass
class AllowedMentions(Base):
  T_ROLE_MENTION: ClassVar[str] = "roles"
  T_USER_MENTIONS: ClassVar[str] = "users"
  T_EVERYONE_MENTIONS: ClassVar[str] = "everyone"

  __FC_ALLOWED_MENTION_TYPE: ClassVar[tuple] = (T_ROLE_MENTION, T_USER_MENTIONS, T_EVERYONE_MENTIONS)

  parse: list[str] | Exclude=EXCLUDE
  roles: list[snowflake] | Exclude=EXCLUDE
  users: list[snowflake] | Exclude=EXCLUDE
  replied_user: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    if isinstance(self.parse, list):
      for p in self.parse:
        format_checker(p, "parse", in_list=self.__FC_ALLOWED_MENTION_TYPE)
    format_checker(self.roles, "roles", 0, 100)
    format_checker(self.users, "users", 0, 100)
    return super().format_check()

@dataclass
class MessageReference(Base):
  T_DEFAULT: ClassVar[int] = 0
  T_FORWARD: ClassVar[int] = 1

  type: int | Exclude=EXCLUDE
  message_id: snowflake | Exclude=EXCLUDE
  channel_id: snowflake | Exclude=EXCLUDE
  guild_id: snowflake | Exclude=EXCLUDE
  fail_if_not_exists: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=(0, 1))
    return super().format_check()

@dataclass
class AttachmentRequest(Base):
  id: snowflake | int
  filename: str | Exclude=EXCLUDE
  title: str | Exclude=EXCLUDE
  description: str | Exclude=EXCLUDE
  duration_secs: float | Exclude=EXCLUDE
  waveform: str | Exclude=EXCLUDE
  is_spoiler: bool | Exclude=EXCLUDE

@dataclass
class ShardClientTheme(Base):
  BT_UNSET: ClassVar[int] = 0
  BT_DARK: ClassVar[int] = 1
  BT_LIGHT: ClassVar[int] = 2
  BT_DARKER: ClassVar[int] = 3
  BT_MIDNIGHT: ClassVar[int] = 4

  __FC_BASE_THEME_TYPE: ClassVar[tuple] = (BT_UNSET, BT_DARK, BT_LIGHT, BT_DARKER, BT_MIDNIGHT)

  colors: list[str]
  gradient_angle: int
  base_mix: int
  base_theme: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.colors, "colors", 0, 5)
    format_checker(self.gradient_angle, "gradient_angle", 0, 360)
    format_checker(self.base_mix, "base_mix", 0, 100)
    format_checker(self.base_theme, "base_theme", in_list=self.__FC_BASE_THEME_TYPE)
    return super().format_check()

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

  content: str | Exclude=EXCLUDE
  nonce: int | str | Exclude=EXCLUDE
  tts: bool | Exclude=EXCLUDE
  embeds: list[Embed] | Exclude=EXCLUDE
  allowed_mentions: AllowedMentions | Exclude=EXCLUDE
  message_reference: MessageReference | Exclude=EXCLUDE
  components: list[component.ComponentClass] | Exclude=EXCLUDE
  sticker_ids: list[snowflake] | Exclude=EXCLUDE
  files: FormFile = field(default_factory=FormFile)
  payload_json: str | Exclude=EXCLUDE
  attachments: list[AttachmentRequest] | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  enforce_nonce: bool | Exclude=EXCLUDE
  poll: b_poll.Poll | Exclude=EXCLUDE
  shared_client_theme: ShardClientTheme | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    format_checker(self.nonce, "nonce", 0, 25)
    format_checker(self.nonce, "embeds", 0, 10)
    format_checker(self.sticker_ids, "sticker_ids", 0, 3)
    return super().format_check()

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

  content: str | None | Exclude=EXCLUDE
  embeds: list[Embed] | None | Exclude=EXCLUDE
  flags: int | None | Exclude=EXCLUDE
  allowed_mentions: AllowedMentions | None | Exclude=EXCLUDE
  components: list[component.ComponentClass] | None | Exclude=EXCLUDE
  files: FormFile = FormFile()
  payload_json: str | None | Exclude=EXCLUDE
  attachments: list[AttachmentRequest] | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    format_checker(self.embeds, "embeds", 0, 10)
    return super().format_check()

@dataclass
class DeleteMessage(__MessageBase):
  req_url:  ClassVar[str] = "/messages/<message.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkDeleteMessages(__MessageBase):
  req_url:  ClassVar[str] = "/messages/bulk-delete"
  req_type: ClassVar[str] = "post"

  messages: list[snowflake]

  def format_check(self) -> None:
    format_checker(self.messages, "messages", 2, 100)
    return super().format_check()

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