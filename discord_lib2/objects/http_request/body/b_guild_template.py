from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
image_data = str
ISO8601timestamp = str
EXCLUDE = Exclude()

@dataclass
class __GuildTemplateBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/templates"

@dataclass
class GetGuildTemplate(body_base.BaseClass):
  req_base_url: ClassVar[str] = ""
  req_url:  ClassVar[str] = "/guilds/templates/<template.code>"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildTemplates(__GuildTemplateBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildTemplate(__GuildTemplateBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  description: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.description, "description", 1, 120)
    return super().format_check()

@dataclass
class SyncGuildTemplate(__GuildTemplateBase):
  req_url:  ClassVar[str] = "/<template.code>"
  req_type: ClassVar[str] = "put"

@dataclass
class ModifyGuildTemplate(__GuildTemplateBase):
  req_url:  ClassVar[str] = "/<template.code>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  description: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.description, "description", 1, 120)
    return super().format_check()

@dataclass
class DeleteGuildTemplate(__GuildTemplateBase):
  req_url:  ClassVar[str] = "/<template.code>"
  req_type: ClassVar[str] = "delete"