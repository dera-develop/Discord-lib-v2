from typing import Literal

from discord_lib2.objects.http_request.body.body_base import Exclude as BE
from discord_lib2.objects.http_request.query.query_base import Exclude as QE

class PayloadFormatError(Exception):
  def __init__(self, key: str, reason: str) -> None:
    super().__init__(f"request payload format error | key: {key}, reason: {reason}")

def _gen_out_of_range(value_type: Literal["number", "string", "list"], min, max) -> str:
  if value_type == "number":
    return f"value out of range (from {min} to {max})"
  if value_type == "string":
    return f"string length out of range (from {min} to {max})"
  if value_type == "list":
    return f"list length out of range (from {min} to {max})"
  return "N/A"

def _gen_invalid_value(value_list: list|tuple) -> str:
  return f"invalid value, must be one of: {value_list}"

def format_checker(value: int|float|str|list|dict|None|BE|QE, value_name: str, value_min: int|float=0, value_max: int|float=0, in_list: list|tuple|None=None) -> None:
  if isinstance(value, int | float | str):
    if in_list is not None:
      if not value in in_list:
        raise PayloadFormatError(value_name, _gen_invalid_value(in_list))
    else:
      if isinstance(value, int | float):
        if not value_min <= value <= value_max:
          raise PayloadFormatError(value_name, _gen_out_of_range("number", value_min, value_max))
      else:
        if not value_min <= len(value) <= value_max:
          raise PayloadFormatError(value_name, _gen_out_of_range("string", value_min, value_max))
  elif isinstance(value, list|dict):
    if not value_min <= len(value) <= value_max:
      raise PayloadFormatError(value_name, _gen_out_of_range("list", value_min, value_max))