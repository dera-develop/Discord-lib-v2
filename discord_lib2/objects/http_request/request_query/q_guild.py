from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str
c_d_snowflake = str

@dataclass
class GetGuild(BaseClass):
  with_counts: bool | Exclude = Exclude()

@dataclass
class ListGuildMembers(BaseClass):
  limit: int | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()

@dataclass
class SearchGuildMembers(BaseClass):
  query: str
  limit: int | Exclude = Exclude()

@dataclass
class GetGuildBans(BaseClass):
  limit: int | Exclude = Exclude()
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()

@dataclass
class GetGuildPruneCount(BaseClass):
  days: int
  include_roles: c_d_snowflake

@dataclass
class GetGuildWidgetImage(BaseClass):
  WSO_SHIELD: ClassVar[str] = "shield"
  WSO_BANNER1: ClassVar[str] = "banner1"
  WSO_BANNER2: ClassVar[str] = "banner2"
  WSO_BANNER3: ClassVar[str] = "banner3"
  WSO_BANNER4: ClassVar[str] = "banner4"

  style: str