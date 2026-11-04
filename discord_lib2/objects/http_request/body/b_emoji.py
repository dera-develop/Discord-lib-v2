from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.other import permissions
from discord_lib2.objects.http_request.body import b_user

snowflake  = str
image_data = str
EXCLUDE = Exclude()

@dataclass
class __EmojiBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/emojis"

@dataclass
class __EmojiApplicationBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications/<application.id>/emojis"

@dataclass
class Emoji(Base):
  id: snowflake | None
  name: str | None
  roles: list[permissions.Role] | Exclude=EXCLUDE
  user: b_user.User | Exclude=EXCLUDE
  require_colons: bool | Exclude=EXCLUDE
  managed: bool | Exclude=EXCLUDE
  animated: bool | Exclude=EXCLUDE
  available: bool | Exclude=EXCLUDE

@dataclass
class ListGuildEmojis(__EmojiBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildEmoji(__EmojiBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildEmoji(__EmojiBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  image: image_data
  roles: list[snowflake]

@dataclass
class ModifyGuildEmoji(__EmojiBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "patch"

  name: str
  roles: list[snowflake] | None

@dataclass
class DeleteGuildEmoji(__EmojiBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class ListApplicationEmojis(__EmojiApplicationBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetApplicationEmoji(__EmojiApplicationBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateApplicationEmoji(__EmojiApplicationBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  image: image_data

@dataclass
class ModifyApplicationEmoji(__EmojiApplicationBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "patch"

  name: str

@dataclass
class DeleteApplicationEmoji(__EmojiApplicationBase):
  req_url:  ClassVar[str] = "/<emoji.id>"
  req_type: ClassVar[str] = "delete"