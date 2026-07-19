from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str
c_d_snowflake = str

@dataclass
class ListEntitlements(BaseClass):
  user_id: snowflake | Exclude = Exclude()
  sku_ids: c_d_snowflake | Exclude = Exclude()
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()
  guild_id: snowflake | Exclude = Exclude()
  exclude_ended: bool | Exclude = Exclude()
  exclude_deleted: bool | Exclude = Exclude()