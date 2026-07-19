from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str

@dataclass
class GetAnswerVoters(BaseClass):
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()