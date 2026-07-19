from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude

snowflake = str
ISO8601timestamp = str

@dataclass
class __VoiceBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/voice-states"

@dataclass
class ListVoiceRegions(body_base.BaseClass):
  req_url:  ClassVar[str] = "/voice/regions"
  req_type: ClassVar[str] = "get"

@dataclass
class GetCurrentUserVoiceState(__VoiceBase):
  req_url:  ClassVar[str] = "/@me"
  req_type: ClassVar[str] = "get"

@dataclass
class GetUserVoiceState(__VoiceBase):
  req_url:  ClassVar[str] = "/<user.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyCurrentUserVoiceState(__VoiceBase):
  req_url:  ClassVar[str] = "/@me"
  req_type: ClassVar[str] = "patch"

  channel_id: snowflake | Exclude = Exclude()
  suppress: bool | Exclude = Exclude()
  request_to_speak_timestamp: ISO8601timestamp | None | Exclude = Exclude()

@dataclass
class ModifyUserViceState(__VoiceBase):
  req_url:  ClassVar[str] = "/<userid>"
  req_type: ClassVar[str] = "patch"