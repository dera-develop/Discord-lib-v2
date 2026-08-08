from typing import ClassVar, Any, Type
from logging import Logger

snowflake = str
ISO8601timestamp = str

class UserCacheBase:
  replaces: ClassVar[dict[str, str]] = {}   # head_key_str: key_path

  def update(self, data: dict):
    pass

class KeyTypeException(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

def __get_key(d, ks: list[str], i=0):
  if d is None:
    return None
  if i >= len(ks):
    return d
  if isinstance(d, dict):
    return __get_key(d.get(ks[i]), ks, i+1)
  else:
    return d

def replace(target_dict: dict[str, Any], target_class: Type[UserCacheBase], logger: Logger | None):
  if target_class.replaces != {}:
    for k, v in target_class.replaces.items():
      list_datas = target_dict.get(k)
      if list_datas is None:
        continue

      if len(list_datas) == 0:
        target_dict[k] = {}
        continue

      if not isinstance(list_datas, list):
        continue

      set_dict = {}
      key_nest = v.split("/")
      for list_data in list_datas:
        if not isinstance(list_data, dict):
          continue

        key = __get_key(list_data, key_nest)
        if not isinstance(key, str):
          if logger is not None:
            logger.error(f"cache parse error | cache: {target_class.__class__.__name__}, key: {k}")
          continue

        set_dict[key] = list_data
      target_dict[k] = set_dict
  return target_dict