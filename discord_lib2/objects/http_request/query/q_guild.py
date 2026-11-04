from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
c_d_snowflake = str

@dataclass
class GetGuild(BaseClass):
  with_counts: bool | Exclude = Exclude()

@dataclass
class ListGuildMembers(BaseClass):
  limit: int | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 1000)

@dataclass
class SearchGuildMembers(BaseClass):
  query: str
  limit: int | Exclude = Exclude()

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 1000)

@dataclass
class GetGuildBans(BaseClass):
  limit: int | Exclude = Exclude()
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 1000)

@dataclass
class GetGuildPruneCount(BaseClass):
  days: int
  include_roles: c_d_snowflake

  def format_check(self) -> None:
    format_checker(self.days, "days", 1, 30)

@dataclass
class GetGuildWidgetImage(BaseClass):
  WSO_SHIELD: ClassVar[str] = "shield"
  WSO_BANNER1: ClassVar[str] = "banner1"
  WSO_BANNER2: ClassVar[str] = "banner2"
  WSO_BANNER3: ClassVar[str] = "banner3"
  WSO_BANNER4: ClassVar[str] = "banner4"

  __FC_WIDGET_STYLE_OPTIONS: ClassVar[tuple] = (WSO_SHIELD, WSO_BANNER1, WSO_BANNER2, WSO_BANNER3, WSO_BANNER4)

  style: str

  def format_check(self) -> None:
    format_checker(self.style, "style", in_list=self.__FC_WIDGET_STYLE_OPTIONS)