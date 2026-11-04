from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
EXCLUDE = Exclude()

@dataclass
class __StageInstanceBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/stage-instances"

@dataclass
class CreateStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  channel_id: snowflake
  topic: str
  privacy_level: int | Exclude=EXCLUDE
  send_start_notification: bool | Exclude=EXCLUDE
  guild_scheduled_event_id: snowflake | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.topic, "topic", 1, 120)
    return super().format_check()

@dataclass
class GetStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "<channel.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "patch"

  topic: str | Exclude=EXCLUDE
  privacy_level: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.topic, "topic", 1, 120)
    return super().format_check()

@dataclass
class DeleteStageInstance(__StageInstanceBase):
  req_url:  ClassVar[str] = "/<channel.id>"
  req_type: ClassVar[str] = "delete"