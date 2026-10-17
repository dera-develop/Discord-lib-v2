from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

snowflake = set

@dataclass
class GetLobbyMessages(BaseClass):
  limit: int | Exclude = Exclude()