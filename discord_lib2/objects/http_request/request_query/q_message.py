from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str
ISO8601timestamp = str

@dataclass
class GetChannelMessages(BaseClass):
  around: snowflake | Exclude = Exclude()
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()

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

  limit: int | Exclude = Exclude()
  offset: int | Exclude = Exclude()
  max_id: snowflake | Exclude = Exclude()
  min_id: snowflake | Exclude = Exclude()
  slop: int | Exclude = Exclude()
  content: str | Exclude = Exclude()
  channel_id: list[snowflake] | Exclude = Exclude()
  author_type: list[str] | Exclude = Exclude()
  author_id: list[snowflake] | Exclude = Exclude()
  mentions: list[snowflake] | Exclude = Exclude()
  mentions_role_id: list[snowflake] | Exclude = Exclude()
  mention_everyone: bool | Exclude = Exclude()
  replied_to_user_id: list[snowflake] | Exclude = Exclude()
  replied_to_message_id: list[snowflake] | Exclude = Exclude()
  pinned: bool | Exclude = Exclude()
  has: list[str] | Exclude = Exclude()
  embed_type: list[str] | Exclude = Exclude()
  embed_provider: list[str] | Exclude = Exclude()
  link_hostname: list[str] | Exclude = Exclude()
  attachment_filename: list[str] | Exclude = Exclude()
  attachment_extension: list[str] | Exclude = Exclude()
  sort_by: str | Exclude = Exclude()
  sort_order: str | Exclude = Exclude()
  include_nsfw: bool | Exclude = Exclude()

@dataclass
class GetReactions(BaseClass):
  type: int | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()

@dataclass
class GetChannelPins(BaseClass):
  before: ISO8601timestamp | Exclude = Exclude()
  limit: int | Exclude = Exclude()