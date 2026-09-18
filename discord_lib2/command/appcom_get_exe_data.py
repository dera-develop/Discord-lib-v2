from typing import Any, Callable, Awaitable
import copy

from discord_lib2.objects.resources import ApplicationCommandResources
from discord_lib2.objects.gateway.recv_event_object import Interaction, ApplicationCommandAutocompleteInteraction

class AppComArgs(dict):
  def __getattr__(self, key: str) -> Any:
    if key in self:
      return self[key]
    else:
      return None

class AppComExeInfomations:
  def __init__(self, func: Callable[[Interaction, ApplicationCommandResources, AppComArgs], Awaitable[None]], args: AppComArgs) -> None:
    self.func: Callable = func
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

  if dc["path"] != "":
    dc["path"] = dc["path"][:-1]
    option_path = dc["path"].split(".")
    client_in_dict = copy.deepcopy(client_data)
    for path in option_path:
      client_in_dict = client_in_dict[path]
    r_func = client_in_dict["__func"]
  else:
    option_path = []
    r_func = client_data["__func"]

  return AppComExeInfomations(
    r_func,
    AppComArgs(dc["args"])
  )

def __get_appcom_autocomplete_path(server_options: list[dict], path: list):
  for option in server_options:
    if "name" in option:
      path.append(option.get("name"))
      __get_appcom_autocomplete_path(option.get("options", []), path)
    else:
      return

def get_autocomplete_func(server_options: list, client_data: dict) -> Callable[[ApplicationCommandAutocompleteInteraction, ApplicationCommandResources], Awaitable[dict[str, str | int | float]]]:
  async def __dummy(interaction: ApplicationCommandAutocompleteInteraction, resources: ApplicationCommandResources) -> dict[str, str | int | float]:
    return {}
  path = []
  __get_appcom_autocomplete_path(server_options, path)
  client_in_dict = copy.deepcopy(client_data)
  func = __dummy
  for i, p in enumerate(path):
    if i == len(path)-1:
      func: Callable[[ApplicationCommandAutocompleteInteraction, ApplicationCommandResources], Awaitable[dict[str, str | int | float]]] = client_in_dict["__ac"][p]
    else:
      client_in_dict = client_in_dict[p]
  return func