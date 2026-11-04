from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass
from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
EXCLUDE = Exclude()

@dataclass
class ListSKUSubscriptions(BaseClass):
  before: snowflake | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE
  user_id: snowflake | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 100)