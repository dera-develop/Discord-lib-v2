"""
Gatewayイベントの構造体（送信側）
"""
import json
from dataclasses import dataclass, is_dataclass
from typing import ClassVar

snowflake = str
bot_token = snowflake

class Exclude:
  pass

def asdict_exclude_filter(obj) -> dict | list:
  if is_dataclass(obj):
    return_dict = {}
    for key, value in obj.__dict__.items():
      if isinstance(value, Exclude):
        continue
      return_dict[key] = asdict_exclude_filter(value)
    return return_dict
  elif isinstance(obj, list):
    return [asdict_exclude_filter(a_obj) for a_obj in obj]
  elif isinstance(obj, dict):
    return {key: asdict_exclude_filter(value) for key, value in obj.items()}
  else:
    return obj

@dataclass
class UserGatewayRequestBase:
  OP: ClassVar[int]

  def get(self) -> str:
    data_payload = asdict_exclude_filter(self)
    return json.dumps({
      "op": self.OP,
      "d": data_payload
    })

@dataclass
class RequestGuildMembers(UserGatewayRequestBase):
  OP: ClassVar[int] = 8

  guild_id: snowflake
  limit: int
  query: str | Exclude = Exclude()
  presences: bool | Exclude = Exclude()
  user_ids: snowflake | list[snowflake] | Exclude = Exclude()
  nonce: str | Exclude = Exclude()

@dataclass
class RequestSoundboardSounds(UserGatewayRequestBase):
  OP: ClassVar[int] = 31

  guild_ids: list[snowflake]

@dataclass
class RequestChannelInfo(UserGatewayRequestBase):
  OP: ClassVar[int] = 43

  guild_id: snowflake
  fields: list[str]