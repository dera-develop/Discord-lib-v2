from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

snowflake = str

@dataclass
class __StageInstanceBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/stage-instances"

@dataclass
class CreateStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  channel_id: snowflake
  topic: str
  privacy_level: int | Exclude = Exclude()
  send_start_notification: bool | Exclude = Exclude()
  guild_scheduled_event_id: snowflake | Exclude = Exclude()

@dataclass
class GetStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "<channel.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  privacy_level: int | Exclude = Exclude()

@dataclass
class DeleteStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "delete"