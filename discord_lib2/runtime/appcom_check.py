from logging import Logger

from discord_lib2.network.http_request.http import HttpRequestController, RequestFailedError
from discord_lib2.network.http_request.request_loader import RequestLoader
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.command.appcom_diffchecker import checker_v2

from discord_lib2.objects.http_request.body import b_application_command
from discord_lib2.objects.http_request.query import q_application_command

async def __get_current_global_appcoms(logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, data_cache: DataCacheVault) -> list | None:
  logger.info("get current global application commands")
  req_data = req_loader.load_request(
    b_application_command.GetGlobalApplicationCommands(),
    q_application_command.GetGlobalApplicationCommands(),
    application_id=data_cache.data.application.id
  )
  try:
    res = await req_con.add_request(req_data)
  except RequestFailedError as e:
    logger.error(f"failed get current application | reason: {e.name}")
    return None
  if not res.ok:
    logger.error(f"failed get current application | reaason: {res.json}")
    return None
  return res.json

async def __request(logger: Logger, data: dict, app_id: str, req_loader: RequestLoader, req_con: HttpRequestController, new: bool|None, edit: bool|None, delete: bool|None) -> bool:
  update_data = data.get("data")
  if not isinstance(update_data, dict):
    return False
  command_id = None
  if new:
    req_body = b_application_command.CreateGlobalApplicationCommand(update_data)
  elif edit:
    req_body = b_application_command.EditGlobalApplicationCommand(update_data)
    command_id = data.get("id")
  elif delete:
    req_body = b_application_command.DeleteGlobalApplicationCommand()
  else:
    logger.error(f"failed request | reason: operation code error")
    return False
  req_data = req_loader.load_request(req_body, application_id=app_id, command_id=command_id)
  try:
    res = await req_con.add_request(req_data)
  except RequestFailedError as e:
    logger.error(f"failed update global application command request | reason: {e.name}")
    return False
  if not res.ok:
    logger.error(f"failed update global application command request | reaason: {res.json}")
    return False
  return True

async def __update(current_appcom: list, new_appcom: list, logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, app_id: str):
  logger.info("updating...")
  global_appcom_datas: list[dict] = checker_v2(current_appcom, new_appcom)
  update_count = {"new": 0, "edit": 0, "delete": 0}
  for data in global_appcom_datas:
    status = await __request(logger, data, app_id, req_loader, req_con, data.get("new"), data.get("edit"), data.get("del"))
    if not status:
      continue
    if data.get("new"):
      update_count["new"] += 1
    elif data.get("edit"):
      update_count["edit"] += 1
    elif data.get("del"):
      update_count["delete"] += 1
  logger.info(f"global command update | new: {update_count['new']}, edit: {update_count['edit']}, delete: {update_count['delete']}")

async def update_global_appcom(logger: Logger, req_loader: RequestLoader, req_con: HttpRequestController, data_cache: DataCacheVault, new_appcom: list) -> bool:
  logger.info("update global application commands")
  current_data = await __get_current_global_appcoms(logger, req_loader, req_con, data_cache)
  if current_data is None:
    return False
  await __update(current_data, new_appcom, logger, req_loader, req_con, data_cache.data.application.id)
  return True