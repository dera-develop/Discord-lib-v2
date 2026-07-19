from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str

@dataclass
class ListSchjeduledEventforGuild(BaseClass):
  with_user_count: bool | Exclude = Exclude()

@dataclass
class GetGuildScheduledEvent(BaseClass):
  with_user_count: bool | Exclude = Exclude()

@dataclass
class GetGuildScheduledEventUsers(BaseClass):
  limit: int | Exclude = Exclude()
  with_member: bool | Exclude = Exclude()
  before: snowflake | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
