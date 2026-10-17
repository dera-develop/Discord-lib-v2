from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

snowflake = str

@dataclass
class GetInvite(BaseClass):
  with_counts: bool | Exclude = Exclude()
  guild_scheduled_event_id: snowflake | Exclude = Exclude()