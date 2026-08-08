from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

snowflake = str

@dataclass
class __SoundboardBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/soundboard-sounds"

@dataclass
class SendSoundboardSound(body_base.BaseClass):
  req_url:  ClassVar[str] = "/channels/<channel.id>/send-soundboard-sound"
  req_type: ClassVar[str] = "post"

  sound_id: snowflake
  source_guild_id: snowflake | Exclude = Exclude()

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
  volume: float | None | Exclude = Exclude()
  emoji_id: snowflake | None | Exclude = Exclude()
  emoji_name: str | None | Exclude = Exclude()

@dataclass
class ModifyGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = "/<sound.id>"
  req_type: ClassVar[str] = "patch"

  name: str | Exclude = Exclude()
  volume: float | None | Exclude = Exclude()
  emoji_id: snowflake | None | Exclude = Exclude()
  emoji_name: str | None | Exclude = Exclude()

@dataclass
class DeleteGuildSoundboardSound(__SoundboardBase):
  req_url:  ClassVar[str] = "/<sound.id>"
  req_type: ClassVar[str] = "delete"