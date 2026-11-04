from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass
from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
ISO8601timestamp = str
EXCLUDE = Exclude()

@dataclass
class GetChannelMessages(BaseClass):
  around: snowflake | Exclude=EXCLUDE
  before: snowflake | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 100)

@dataclass
class SearchGuildMessages(BaseClass):
  AT_USER: ClassVar[str] = "user"
  AT_BOT: ClassVar[str] = "bot"
  AT_WEBHOOK: ClassVar[str] = "webhook"

  SHT_IMAGE: ClassVar[str] = "image"
  SHT_SOUND: ClassVar[str] = "sound"
  SHT_VIDEO: ClassVar[str] = "video"
  SHT_FILE: ClassVar[str] = "file"
  SHT_STICKER: ClassVar[str] = "sticker"
  SHT_EMBED: ClassVar[str] = "embed"
  SHT_LINK: ClassVar[str] = "link"
  SHT_POLL: ClassVar[str] = "poll"
  SHT_SNAPSHOT: ClassVar[str] = "snapshot"

  SET_IMAGE: ClassVar[str] = "image"
  SET_VIDEO: ClassVar[str] = "video"
  SET_GIF: ClassVar[str] = "gif"
  SET_SOUND: ClassVar[str] = "sound"
  SET_ARTICLE: ClassVar[str] = "article"

  SSM_TIMESTAMP: ClassVar[str] = "timestamp"
  SSM_RELEVANCE: ClassVar[str] = "relevance"

  __FC_AUTHOR_TYPE: ClassVar[tuple] = (AT_USER, AT_BOT, AT_WEBHOOK)
  __FC_SEARCH_HAS_TYPE: ClassVar[tuple] = (SHT_IMAGE, SHT_SOUND, SHT_VIDEO, SHT_FILE, SHT_STICKER, SHT_EMBED, SHT_LINK, SHT_POLL, SHT_SNAPSHOT)
  __FC_EMBED_TYPE: ClassVar[tuple] = ("image", "video", "gif", "sound", "article")
  __FC_SEARCH_SORT_MODE: ClassVar[tuple] = (SSM_TIMESTAMP, SSM_RELEVANCE)

  limit: int | Exclude=EXCLUDE
  offset: int | Exclude=EXCLUDE
  max_id: snowflake | Exclude=EXCLUDE
  min_id: snowflake | Exclude=EXCLUDE
  slop: int | Exclude=EXCLUDE
  content: str | Exclude=EXCLUDE
  channel_id: list[snowflake] | Exclude=EXCLUDE
  author_type: list[str] | Exclude=EXCLUDE
  author_id: list[snowflake] | Exclude=EXCLUDE
  mentions: list[snowflake] | Exclude=EXCLUDE
  mentions_role_id: list[snowflake] | Exclude=EXCLUDE
  mention_everyone: bool | Exclude=EXCLUDE
  replied_to_user_id: list[snowflake] | Exclude=EXCLUDE
  replied_to_message_id: list[snowflake] | Exclude=EXCLUDE
  pinned: bool | Exclude=EXCLUDE
  has: list[str] | Exclude=EXCLUDE
  embed_type: list[str] | Exclude=EXCLUDE
  embed_provider: list[str] | Exclude=EXCLUDE
  link_hostname: list[str] | Exclude=EXCLUDE
  attachment_filename: list[str] | Exclude=EXCLUDE
  attachment_extension: list[str] | Exclude=EXCLUDE
  sort_by: str | Exclude=EXCLUDE
  sort_order: str | Exclude=EXCLUDE
  include_nsfw: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 25)
    format_checker(self.offset, "offset", 0, 9975)
    format_checker(self.slop, "slop", 0, 100)
    format_checker(self.content, "content", 0, 1024)
    format_checker(self.channel_id, "channel_id", 0, 500)
    format_checker(self.author_id, "author_id", 0, 100)
    format_checker(self.mentions, "mentions", 0, 100)
    format_checker(self.mentions_role_id, "mentions_role_id", 0, 100)
    format_checker(self.replied_to_user_id, "replied_to_user_id", 0, 100)
    format_checker(self.replied_to_message_id, "replied_to_message_id", 0, 100)
    format_checker(self.has, "has", in_list=self.__FC_SEARCH_HAS_TYPE)
    format_checker(self.embed_type, "embed_type", in_list=self.__FC_EMBED_TYPE)
    format_checker(self.embed_provider, "embed_provider", 0, 100)
    format_checker(self.link_hostname, "link_hostname", 0, 100)
    format_checker(self.attachment_filename, "attachment_filename", 0, 100)
    format_checker(self.attachment_extension, "attachment_extension", 0, 100)
    format_checker(self.sort_by, "sort_by", in_list=self.__FC_SEARCH_SORT_MODE)
    format_checker(self.sort_order, "sort_order", in_list=("asc", "desc"))
    if isinstance(self.author_type, list):
      for t in self.author_type:
       format_checker(t, "author_type", in_list=self.__FC_AUTHOR_TYPE)
    if isinstance(self.embed_provider, list):
      for e in self.embed_provider:
        format_checker(e, "embed_provider", 0, 256)
    if isinstance(self.link_hostname, list):
      for e in self.link_hostname:
        format_checker(e, "link_hostname", 0, 256)
    if isinstance(self.attachment_filename, list):
      for e in self.attachment_filename:
        format_checker(e, "attachment_filename", 0, 1024)
    if isinstance(self.attachment_extension, list):
      for e in self.attachment_extension:
        format_checker(e, "attachment_extension", 0, 256)

@dataclass
class GetReactions(BaseClass):
  type: int | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=(0, 1))
    format_checker(self.limit, "limit", 1, 100)

@dataclass
class GetChannelPins(BaseClass):
  before: ISO8601timestamp | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 50)