from logging import Logger
from typing import Literal

from discord_lib2.network.http_request.http import HttpRequestController, RequestFailedError
from discord_lib2.network.http_request.request_loader import RequestLoader
from discord_lib2.command.appcom_diffchecker import checker_v2

from discord_lib2.objects.http_request.body import b_application_command
from discord_lib2.objects.http_request.query import q_application_command

async def __get_current_appcoms(logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, app_id: str, guild_id: str|None=None) -> list | None:
  if guild_id is None:
    req_body  = b_application_command.GetGlobalApplicationCommands()
    req_query = q_application_command.GetGlobalApplicationCommands(with_localizations=True)
  else:
    req_body  = b_application_command.GetGuildApplicationCommands()
    req_query = q_application_command.GetGuildApplicationCommands(with_localizations=True)
  req_data = req_loader.load_request(req_body, req_query, application_id=app_id, guild_id=guild_id)
  try:
    res = await req_con.add_request(req_data)
  except RequestFailedError as e:
    logger.error(f"failed get current {"global" if guild_id is None else "guild"} application command | reason: {e.name}")
    return None
  if not res.ok:
    logger.error(f"failed get current {"global" if guild_id is None else "guild"} application command | reason: {res.json}")
    return None
  return res.json

async def __send_update_request(logger: Logger, data: dict, app_id: str, req_loader: RequestLoader, req_con: HttpRequestController, guild_id: str|None=None) -> bool:
  command_id: str | None = data.get("id")
  if data.get("new"):
    update_data: dict = data["data"]
    if guild_id is None:  req_body = b_application_command.CreateGlobalApplicationCommand(update_data)
    else:                 req_body = b_application_command.CreateGuildApplicationCommand(update_data)
  elif data.get("edit"):
    update_data: dict = data["data"]
    if guild_id is None:  req_body = b_application_command.EditGlobalApplicationCommand(update_data)
    else:                 req_body = b_application_command.EditGuildApplicationCommand(update_data)
  elif data.get("del"):
    if guild_id is None:  req_body = b_application_command.DeleteGlobalApplicationCommand()
    else:                 req_body = b_application_command.DeleteGuildApplicationCommand()
  else:
    logger.error(f"failed request | reason: update operation code error")
    return False
  req_data = req_loader.load_request(req_body, application_id=app_id, guild_id=guild_id, command_id=command_id)
  try:
    res = await req_con.add_request(req_data)
  except RequestFailedError as e:
    logger.error(f"failed get current {"global" if guild_id is None else "guild"} application command | reason: {e.name}")
    return False
  if not res.ok:
    logger.error(f"failed get current {"global" if guild_id is None else "guild"} application command | reason: {res.json}")
    return False
  return True

async def __check_update(current_appcom: list, new_appcoms: list, logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, app_id: str, guild_id: str|None=None):
  appcom_diff_data: list[dict] = checker_v2(current_appcom, new_appcoms)
  update_count = {"new": 0, "edit": 0, "delete": 0}
  for data in appcom_diff_data:
    status = await __send_update_request(logger, data, app_id, req_loader, req_con, guild_id)
    if not status:
      continue
    if data.get("new"):
      update_count["new"] += 1
    elif data.get("edit"):
      update_count["edit"] += 1
    elif data.get("del"):
      update_count["delete"] += 1
  logger.info(f"command update | {f"guild: {guild_id}, "if guild_id is not None else ""}new: {update_count['new']}, edit: {update_count['edit']}, delete: {update_count['delete']}")


async def update_appcom(logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, app_id: str, new_appcoms: list, guild_id: str|None=None) -> bool:
  """
  Update application commands
  guild_id is None, global application command update
  guild_id is not none(snowflake string), guild application command update
  """
  logger.info(f"update {"global" if guild_id is None else "guild"} application commands")
  current_appcoms = await __get_current_appcoms(logger, req_loader, req_con, app_id, guild_id)
  if current_appcoms is None:
    return False
  await __check_update(current_appcoms, new_appcoms, logger, req_loader, req_con, app_id, guild_id)
  return True