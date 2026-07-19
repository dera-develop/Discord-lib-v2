from dataclasses import dataclass
from typing import NewType, ClassVar

from discord_lib2.objects.http_request.base import body_base

snowflake = NewType("snowflake", str)

@dataclass
class __SubscriptionBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/skus/<sku.id>/subscriptions"

@dataclass
class ListSKUSubscriptions(__SubscriptionBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetSKUSubscription(__SubscriptionBase):
  req_url:  ClassVar[str] = "/<subscription.id>"
  req_type: ClassVar[str] = "get"