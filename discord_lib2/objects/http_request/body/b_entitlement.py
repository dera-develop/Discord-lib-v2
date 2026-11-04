from dataclasses import dataclass
from typing import Literal, ClassVar

from discord_lib2.objects.http_request.body import body_base

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str

@dataclass
class __EntitlementBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications/<application.id>/entitlements"


@dataclass
class ListEntitlements(__EntitlementBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"


@dataclass
class GetEntitlement(__EntitlementBase):
  req_url:  ClassVar[str] = "/<entitlement.id>"
  req_type: ClassVar[str] = "get"


@dataclass
class ConsumeanEntitlement(__EntitlementBase):
  req_url:  ClassVar[str] = "/<entitlement.id>/consume"
  req_type: ClassVar[str] = "post"


@dataclass
class CreateTestentitlement(__EntitlementBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  sku_id: str
  owner_id: str
  owner_type: Literal[1, 2]

  def format_check(self) -> None:
    format_checker(self.owner_type, "owner_type", in_list=[1, 2])
    return super().format_check()


@dataclass
class DeleteTestEntitlement(__EntitlementBase):
  req_url:  ClassVar[str] = "/<entitlement.id>"
  req_type: ClassVar[str] = "delete"