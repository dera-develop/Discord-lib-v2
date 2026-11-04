from dataclasses import dataclass
from typing import NewType

from discord_lib2.objects.http_request.query.query_base import BaseClass, Exclude
from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = NewType("snowflake", str)
EXCLUDE = Exclude()

@dataclass
class GetCurrentUserGuilds(BaseClass):
  before: snowflake | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE
  with_counts: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 200)