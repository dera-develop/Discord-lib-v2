from typing import Any, Literal

from discord_lib2.objects.resources import UserEventResources, ApplicationCommandResources, UserTerminalCommandResources
from discord_lib2.Network.http_request.request_loader import RequestInformation

from discord_lib2.objects.gateway import recv_event_object
from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body import b_message

def __load_request_from_dict(req_dict: dict, cls: type[body_base.BaseClass], url_args: dict[str, str]):
  req_infos = RequestInformation("", "", "", True)
  req_infos.request_type = cls.req_type
  req_infos.request_need_token = cls.req_need_token
  req_infos.request_body = req_dict

  base_url = "https://discord.com/api/v10"
  fusion_url = f"{base_url}{cls.req_base_url}{cls.req_url}".strip()
  new_url_args = []
  for arg in fusion_url.split("/"):
    if arg in url_args:
      new_url_args.append(url_args[arg])
    else:
      new_url_args.append(arg)
  req_infos.request_url = "/".join(new_url_args)
  return req_infos

# objects
class Embed:
  __req_dict = {}
  def __get_locals(self, local_values: dict):
    ret_dict = {}
    for key, value in local_values.items():
      if key != "self":
        if value is not None:
          ret_dict[key] = value
    return ret_dict

  def __init__(
      self,
      title: str | None=None,
      type: Literal["rich", "image", "video", "gifv", "article", "link", "poll", "result"] | None=None,
      description: str | None=None,
      url: str | None=None,
      timestamp: str | None=None,
      color: int | None=None,
      flags: int | None=None
  ) -> None:
    self.__req_dict = self.__get_locals(locals())

  def set_footer(
      self,
      text: str,
      icon_url: str | None=None,
      proxy_icon_url: str | None=None
  ) -> None:
    self.__req_dict["footer"] = self.__get_locals(locals())

  def set_image(
      self,
      url: str,
      proxy_url: str | None=None,
      height: int | None=None,
      width: int | None=None,
      content_type: str | None=None,
      placeholder: str | None=None,
      placeholder_version: int | None=None,
      description: str | None=None,
      flags: Literal[32, None]=None
  ) -> None:
    self.__req_dict["image"] = self.__get_locals(locals())

  def set_thumbnail(
      self,
      url: str,
      proxy_url: str | None=None,
      height: int | None=None,
      width: int | None=None,
      content_type: str | None=None,
      placeholder: str | None=None,
      placeholder_version: int | None=None,
      description: str | None=None,
      flags: Literal[32, None]=None
  ) -> None:
    self.__req_dict["image"] = self.__get_locals(locals())

  def set_video(
      self,
      url: str | None=None,
      proxy_url: str | None=None,
      height: int | None=None,
      width: int | None=None,
      context_type: str | None=None,
      placeholder: str | None=None,
      placeholder_version: int | None=None,
      description: str | None=None,
      flags: int | None=None
  ) -> None:
    self.__req_dict["video"] = self.__get_locals(locals())

  def set_provider(
      self,
      name: str | None=None,
      url: str | None=None
  ) -> None:
    self.__req_dict["provider"] = self.__get_locals(locals())

  def set_author(
      self,
      name: str,
      url: str | None=None,
      icon_url: str | None=None,
      proxy_icon_url: str | None=None
  ) -> None:
    self.__req_dict["author"] = self.__get_locals(locals())

  def add_field(
      self,
      name: str,
      value: str,
      inline: bool | None=None
  ) -> None:
    if not "fields" in self.__req_dict:
      self.__req_dict["fields"] = []
    self.__req_dict["fields"].append(self.__get_locals(locals()))

  async def send(
      self,
      resources: UserEventResources | UserTerminalCommandResources | ApplicationCommandResources,
      channel_id: str
  ) -> bool:
    req_data = __load_request_from_dict(self.__req_dict, b_message.CreateMessage, {"<channel.id>": channel_id})
    res = await resources.http_api.request(req_data)
    return res.ok

  async def reply(
      self,
      resources: UserEventResources | UserTerminalCommandResources | ApplicationCommandResources,
      message_create_object: recv_event_object.MessageCreateUpdate
  ) -> bool:
    if message_create_object.channel_id is None:
      return False
    req_data = __load_request_from_dict(self.__req_dict, b_message.CreateMessage, {"<channel.id>": message_create_object.channel_id})
    res = await resources.http_api.request(req_data)
    return res.ok

# functions
async def send_message(
    resources: UserEventResources | UserTerminalCommandResources | ApplicationCommandResources,
    message: str,
    channel_id: str
) -> bool:
  req_data = resources.http_api.load_request(
    b_message.CreateMessage(content=message),
    channel_id=channel_id
  )
  res = await resources.http_api.request(req_data)
  return res.ok

async def reply_message(
    resources: UserEventResources | UserTerminalCommandResources | ApplicationCommandResources,
    message_create_object: recv_event_object.MessageCreateUpdate,
    message: str
) -> bool:
  req_data = resources.http_api.load_request(
    b_message.CreateMessage(content=message, message_reference=b_message.MessageReference(type=0, message_id=message_create_object.id)),
    channel_id=message_create_object.channel_id
  )
  res = await resources.http_api.request(req_data)
  return res.ok