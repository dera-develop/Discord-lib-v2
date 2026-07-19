from dataclasses import dataclass
from typing import Literal, ClassVar

from discord_lib2.objects.http_request.base import body_base

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


@dataclass
class DeleteTestEntitlement(__EntitlementBase):
  req_url:  ClassVar[str] = "/<entitlement.id>"
  req_type: ClassVar[str] = "delete"