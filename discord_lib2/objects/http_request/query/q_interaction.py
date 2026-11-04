from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

snowflake = str
EXCLUDE = Exclude()

@dataclass
class CreateInteractionResponse(BaseClass):
  with_response: bool | Exclude=EXCLUDE

@dataclass
class CreateFollowupMessage(BaseClass):
  wait: bool
  thread_id: snowflake
  with_components: bool