from dataclasses import dataclass, field
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, FormFile

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
EXCLUDE = Exclude()

@dataclass
class __StickerBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/stickers"

@dataclass
class GetSticker(body_base.BaseClass):
  req_url:  ClassVar[str] = "/stickers/<sticker.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ListStickerPacks(body_base.BaseClass):
  req_url:  ClassVar[str] = "/sticker-packs"
  req_type: ClassVar[str] = "get"

@dataclass
class GetStickerPack(body_base.BaseClass):
  req_url:  ClassVar[str] = "/sticker-packs/<pack.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ListGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = "/<sticker.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateguildSticker(__StickerBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  description: str
  tags: str
  file: FormFile = field(default_factory=FormFile)

  def format_check(self) -> None:
    format_checker(self.name, "name", 2, 30)
    format_checker(self.description, "description", 2, 100)
    format_checker(self.tags, "tags", 0, 200)
    return super().format_check()

@dataclass
class ModifyGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = "/<sticker.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  description: str | None | Exclude=EXCLUDE
  tags: str | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 2, 30)
    format_checker(self.description, "description", 2, 100)
    format_checker(self.tags, "tags", 0, 200)
    return super().format_check()

@dataclass
class DeleteGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = "/<sticker.id>"
  req_type: ClassVar[str] = "delete"