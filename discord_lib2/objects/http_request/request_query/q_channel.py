from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

snowflake = str
ISO8601timestamp = str

@dataclass
class GetThreadMember(BaseClass):
  with_member: bool | Exclude = Exclude()

@dataclass
class ListThreadMember(BaseClass):
  with_member: bool | Exclude = Exclude()
  after: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()

@dataclass
class ListPublicArchivedThreads(BaseClass):
  before: ISO8601timestamp | Exclude = Exclude()
  limit: int | Exclude = Exclude()

@dataclass
class ListJoinedPrivateArchivedThreads(BaseClass):
  before: snowflake | Exclude = Exclude()
  limit: int | Exclude = Exclude()