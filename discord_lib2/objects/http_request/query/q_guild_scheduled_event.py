from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
EXCLUDE = Exclude()

@dataclass
class ListSchjeduledEventforGuild(BaseClass):
  with_user_count: bool | Exclude=EXCLUDE

@dataclass
class GetGuildScheduledEvent(BaseClass):
  with_user_count: bool | Exclude=EXCLUDE

@dataclass
class GetGuildScheduledEventUsers(BaseClass):
  limit: int | Exclude=EXCLUDE
  with_member: bool | Exclude=EXCLUDE
  before: snowflake | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 0, 100)