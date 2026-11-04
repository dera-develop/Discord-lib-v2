from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
EXCLUDE = Exclude()

@dataclass
class __SoundboardBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/soundboard-sounds"

@dataclass
class SendSoundboardSound(body_base.BaseClass):
  req_url:  ClassVar[str] = "/channels/<channel.id>/send-soundboard-sound"
  req_type: ClassVar[str] = "post"

  sound_id: snowflake
  source_guild_id: snowflake | Exclude=EXCLUDE

@dataclass
class ListDefaultSoundboardSounds(body_base.BaseClass):
  req_url:  ClassVar[str] = "/soundboard-default-sounds"
  req_type: ClassVar[str] = "get"

@dataclass
class ListGuildSoundboardSounds(__SoundboardBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = "/<sound.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  sound: str
  volume: float | None | Exclude=EXCLUDE
  emoji_id: snowflake | None | Exclude=EXCLUDE
  emoji_name: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 2, 32)
    format_checker(self.volume, "volume", 0, 1)
    return super().format_check()

@dataclass
class ModifyGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = "/<sound.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude=EXCLUDE
  volume: float | None | Exclude=EXCLUDE
  emoji_id: snowflake | None | Exclude=EXCLUDE
  emoji_name: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 2, 32)
    format_checker(self.volume, "volume", 0, 1)
    return super().format_check()

@dataclass
class DeleteGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = "/<sound.id>"
  req_type: ClassVar[str] = "delete"