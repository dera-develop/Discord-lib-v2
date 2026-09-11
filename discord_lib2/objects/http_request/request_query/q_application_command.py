from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import Exclude, BaseClass

@dataclass
class GetGlobalApplicationCommands(BaseClass):
  with_localizations: bool | Exclude = Exclude()
  
@dataclass
class GetGuildApplicationCommands(BaseClass):
  with_localizations: bool | Exclude = Exclude()