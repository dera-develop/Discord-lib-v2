from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

@dataclass
class CreateInteractionResponse(BaseClass):
  with_response: bool | Exclude = Exclude()