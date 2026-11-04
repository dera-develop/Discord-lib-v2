from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import Exclude, BaseClass

EXCLUDE = Exclude()

@dataclass
class GetGlobalApplicationCommands(BaseClass):
  with_localizations: bool | Exclude=EXCLUDE
  
@dataclass
class GetGuildApplicationCommands(BaseClass):
  with_localizations: bool | Exclude=EXCLUDE