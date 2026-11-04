from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
c_d_snowflake = str
EXCLUDE = Exclude()

@dataclass
class ListEntitlements(BaseClass):
  user_id: snowflake | Exclude=EXCLUDE
  sku_ids: c_d_snowflake | Exclude=EXCLUDE
  before: snowflake | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE
  guild_id: snowflake | Exclude=EXCLUDE
  exclude_ended: bool | Exclude=EXCLUDE
  exclude_deleted: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 100)