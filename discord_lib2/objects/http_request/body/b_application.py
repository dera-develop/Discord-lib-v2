from dataclasses import dataclass
from typing import Literal, ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

base64icon = str
snowflake  = str
ISO8601timestamp = str

@dataclass
class __ApplicationBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications"

@dataclass
class GetCurrentApplication(__ApplicationBase):
  req_url: ClassVar[str] = "/@me"
  req_type: ClassVar[str] = "get"

@dataclass
class GetApplicationActivityInstance(__ApplicationBase):
  req_url: ClassVar[str] = "/<application.id>/activity-instances/<instance.id>"
  req_type: ClassVar[str] = "get"