from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str

@dataclass
class ListSKUSubscriptions(BaseClass):
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()
  user_id: snowflake | Exclude = Exclude()