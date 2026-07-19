from dataclasses import dataclass
from typing import NewType

from discord_lib2.objects.http_request.request_query.query_base import BaseClass

snowflake = NewType("snowflake", str)

@dataclass
class GetCurrentUserGuilds(BaseClass):
  before: snowflake
  after: snowflake
  limit: int
  with_counts: bool