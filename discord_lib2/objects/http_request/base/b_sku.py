from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base

@dataclass
class ListSKUs(body_base.BaseClass):
  req_url:  ClassVar[str] = "/applications/<application.id>/skus"
  req_type: ClassVar[str] = "get"