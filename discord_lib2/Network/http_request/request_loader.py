from typing import Any
from urllib.parse import urlencode
import uuid
import json

from discord_lib2.logger import Logger

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.request_query import query_base

class RequestInformation:
  def __init__(self, req_url: str, req_type: str, req_body: Any, req_need_token: bool) -> None:
    self.request_url: str = req_url
    self.request_type: str = req_type
    self.request_body: Any = req_body
    self.request_need_token: bool = req_need_token
    self.request_id: uuid.UUID
    self.request_files: dict

class RequestLoader:
  def __init__(self, logger: Logger) -> None:
    self.logger = logger.get_child("HRL")

  def request_load(
      self,
      request_object: body_base.BaseClass,
      request_query_object: query_base.BaseClass | None = None,
      application_id: str | None=None,
      instance_id: str | None=None,
      guild_id: str | None=None,
      auto_moderation_rule_id: str | None=None,
      channel_id: str | None=None,
      overwrite_id: str | None=None,
      user_id: str | None=None,
      message_id: str | None=None,
      emoji_id: str | None=None,
      entitlement_id: str | None=None,
      guild_scheduled_event_id: str | None=None,
      template_code: str | None=None,
      role_id: str | None=None,
      integration_id: str | None=None,
      interaction_id: str | None=None,
      interaction_token: str | None=None,
      invite_code: str | None=None,
      lobby_id: str | None=None,
      answer_id: str | None=None,
      sound_id: str | None=None,
      sticker_id: str | None=None,
      pack_id: str | None=None,
      sku_id: str | None=None,
      subscription_id: str | None=None,
      webhook_id: str | None=None,
      webhook_token: str | None=None) -> RequestInformation:
    
    local_valiable_args = locals()

    url_variable_dict = {}
    for key, value in local_valiable_args.items():
      if key in ("self", "request_object", "request_query_object"):
        continue
      d_key = ".".join(key.rsplit("_", 1))
      url_variable_dict[d_key] = value

    # request body
    try:
      request_body = request_object.get()
      if isinstance(request_body, list):
        raise TypeError(dict)
    except TypeError:
      self.logger.exception("Request object error | type error")
      return RequestInformation("---", "---", "---", False)
    except FileNotFoundError:
      self.logger.exception("Request object error | file not found")
      return RequestInformation("---", "---", "---", False)
    
    file_datas = request_object.get_files()
    
    # request url
    base_url = "https://discord.com/api/v10"
    fusion_url = f"{base_url}{request_object.req_base_url}{request_object.req_url}".strip()
    new_url_args = []
    for arg in fusion_url.split("/"):
      if len(arg) >= 2 and arg[0] == "<" and arg[-1] == ">":
        variable_name = arg[1:-1]
        if url_variable_dict[variable_name] is None:
          raise body_base.PayloadFormatError(f"'{variable_name}': Invalid URL argument.")
        new_url_args.append(str(url_variable_dict[variable_name]).strip())
      else:
        new_url_args.append(arg)
    request_url = "/".join(new_url_args)

    # request query
    request_query = None
    if request_query_object is not None:
      request_query = request_query_object.get()
    
    if request_query is not None:
      if len(request_query) >= 1:
        query_string = f"?{urlencode(request_query)}"
        request_url = f"{request_url}{query_string}"

    request_information = RequestInformation(
      req_url=request_url,
      req_type=request_object.req_type,
      req_body=request_body,
      req_need_token=request_object.req_need_token
    )

    if file_datas != {}:
      request_information.request_files = file_datas
      request_information.request_type = f"{request_object.req_type}_form"
      request_information.request_body = {"payload_json": json.dumps(request_body)}

    return request_information

