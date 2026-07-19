from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base

@dataclass
class __GatewayBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/gateway"

@dataclass
class GetGateway(__GatewayBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

  req_need_token: ClassVar[bool] = False

@dataclass
class GetGatewayBot(__GatewayBase):
  req_url:  ClassVar[str] = "/bot"
  req_type: ClassVar[str] = "get"