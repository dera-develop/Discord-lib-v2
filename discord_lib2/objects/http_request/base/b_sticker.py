from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude
from discord_lib2.objects.http_request.base.body_base import FormFile

snowflake = str

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
  file: FormFile = FormFile()

@dataclass
class ModifyGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = "/<sticker.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude = Exclude()
  description: str | None | Exclude = Exclude()
  tags: str | Exclude = Exclude()

@dataclass
class DeleteGuildSticker(__StickerBase):
  req_url:  ClassVar[str] = "/<sticker.id>"
  req_type: ClassVar[str] = "delete"