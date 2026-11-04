from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass
from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = set
EXCLUDE = Exclude()

@dataclass
class GetLobbyMessages(BaseClass):
  limit: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 200)