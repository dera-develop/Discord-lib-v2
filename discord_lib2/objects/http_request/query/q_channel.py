from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
ISO8601timestamp = str
EXCLUDE = Exclude()

@dataclass
class GetThreadMember(BaseClass):
  with_member: bool | Exclude=EXCLUDE

@dataclass
class ListThreadMember(BaseClass):
  with_member: bool | Exclude=EXCLUDE
  after: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.limit, "limit", 1, 100)

@dataclass
class ListPrivateArchivedThreads(BaseClass):
  before: ISO8601timestamp | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

@dataclass
class ListPublicArchivedThreads(BaseClass):
  before: ISO8601timestamp | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE

@dataclass
class ListJoinedPrivateArchivedThreads(BaseClass):
  before: snowflake | Exclude=EXCLUDE
  limit: int | Exclude=EXCLUDE