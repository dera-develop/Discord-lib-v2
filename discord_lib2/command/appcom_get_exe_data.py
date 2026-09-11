from typing import Any, Callable, Awaitable
from discord_lib2.objects.resources import ApplicationCommandResources
from discord_lib2.objects.http_request.body import b_interaction
from discord_lib2.objects.gateway.recv_event_object import Interaction

class AppComArgs(dict):
  def __getattr__(self, key: str) -> Any:
    if key in self:
      return self[key]
    else:
      return None

class AppComExeInfomations:
  def __init__(self, func: Callable[[Interaction, ApplicationCommandResources, AppComArgs], Awaitable[None]], imsg: b_interaction.InteractionCallbackData | None, it: int, args: AppComArgs) -> None:
    self.func: Callable = func
    self.imsg: b_interaction.InteractionCallbackData | None = imsg  # interaction callback data
    self.it: int = it                                               # interaction type
    self.args: AppComArgs = args

def __get(options: list, return_dict: dict):
  for option in options:
    if option["type"] == 1 or option["type"] == 2:
      return_dict["path"] += f"{option["name"]}."
      __get(option["options"], return_dict)
      return
    else:
      return_dict["args"][option["name"]] = option["value"]

def get_appcom_exedata(server_options: list, client_data: dict):
  dc = {
    "path": "",
    "args": {}
  }
  __get(server_options, dc)

  r_func = None
  r_it = 1
  r_imsg = None

  if dc["path"] != "":
    dc["path"] = dc["path"][:-1]
    option_path = dc["path"].split(".")
    client_in_dict = client_data
    for path in option_path:
      client_in_dict = client_in_dict[path]
    r_func = client_in_dict["__func"]
    r_it = client_in_dict["__itype"]
    r_imsg =client_in_dict["__imsg"]
  else:
    option_path = []
    r_func = client_data["__func"]
    r_it = client_data["__itype"]
    r_imsg = client_data["__imsg"]

  return AppComExeInfomations(
    r_func,
    r_imsg,
    r_it,
    AppComArgs(dc["args"])
  )