from dataclasses import dataclass, is_dataclass
from typing import ClassVar
import os
import mimetypes
import asyncio

class Exclude:
  pass

class FormFile(Exclude):
  def __init__(self) -> None:
    self.files = {}

  def __get_file_binary(self, file_path):
    with open(file_path, "rb") as f:
      return f.read()

  async def add_file(self, file_path: str) -> None:
    file_name = os.path.basename(file_path)
    file_type = mimetypes.guess_type(file_path)[0]
    if file_type is None:
      file_type = "application/octet-stream"
    file_data = await asyncio.to_thread(self.__get_file_binary, file_path)

    file_index = len(self.files)
    self.files[f"files[{file_index}]"] = (
      file_name,
      file_data,
      file_type
    )


class RequestContentType:
  application_json: ClassVar[str] = "application/json"
  application_xwfu: ClassVar[str] = "application/x-www-form-urlencoded"
  multipart_form_data: ClassVar[str] = "multipart/form-data"

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
  
def asdict_file_filter(obj) -> dict:
  files_dict = {}

  if is_dataclass(obj):
    for key, value in obj.__dict__.items():
      if key == "files" and isinstance(value, FormFile):
        files_dict.update(value.files)
  return files_dict

@dataclass
class BaseClass:
  req_base_url: ClassVar[str] = ""
  req_url: ClassVar[str] = ""
  req_type: ClassVar[str] = ""
  req_need_token: ClassVar[bool] = True

  def format_check(self, filtered_dict) -> None:
    pass
  
  def get_files(self):
    return asdict_file_filter(self)

  def get(self) -> dict | list:
    class_dict = asdict_exclude_filter(self)
    self.format_check(class_dict)
    return class_dict
  
class PayloadFormatError(Exception):
  def __init__(self, error_str: str) -> None:
    super().__init__(error_str)