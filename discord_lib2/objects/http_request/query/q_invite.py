from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

snowflake = str
EXCLUDE = Exclude()

@dataclass
class GetInvite(BaseClass):
  with_counts: bool | Exclude=EXCLUDE
  guild_scheduled_event_id: snowflake | Exclude=EXCLUDE