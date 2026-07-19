import requests
import asyncio
import uuid

from discord_lib2.logger import Logger
from discord_lib2.Network.http_request.request_loader import RequestInformation
from discord_lib2.cache.system import system

class RequestQueue(asyncio.Queue):
  async def put(self, item: RequestInformation) -> None:
    return await super().put(item)
  
  async def get(self) -> RequestInformation:
    return await super().get()

class HttpRequestController:
  __task_request_worker = None
  __RESPONCE_HEADER_RATELIMIT = "X-RateLimit-Remaining"
  __RESPONCE_HEADER_RATELIMIT_WAITTIME = "X-RateLimit-Reset-After"

  __REQUEST_HEADER_CONTENT_TYPE_JSON = "application/json"
  __REQUEST_HEADER_CONTENT_TYPE_FORM = "multipart/form-data"

  def __init__(self, system_cache: system.SystemCacheVault, logger: Logger) -> None:
    self.system_cache_vault = system_cache
    self.logger = logger.get_child("HRC")

    self.request_queue = RequestQueue()
    self.responce_data: dict[uuid.UUID, requests.Response] = {}

    self.request_functions = {
      "post":   self.__req_post,
      "get":    self.__req_get,
      "put":    self.__req_put,
      "patch":  self.__req_patch,
      "delete": self.__req_delete
    }
    self.request_functions_form = {
      "post_form" : self.__req_post_form,
      "put_form"  : self.__req_put_form,
      "patch_form": self.__req_patch_form
    }

  def __header(self, content_type: str, enable_token: bool):
    header = {
      "User-Agent": f"DiscordBot (https://github.com/dera-develop/Discord-lib-v2), 2.0",
      "Content-Type": content_type
    }
    if content_type == self.__REQUEST_HEADER_CONTENT_TYPE_FORM:
      header.pop("Content-Type")
    if enable_token:
      header["Authorization"] = f"Bot {self.system_cache_vault.bot_token}"
    return header

  ## JSON ##
  def __req_post(self, url: str, header: dict, data: dict) -> requests.Response:
    return requests.post(url=url, headers=header, json=data)

  def __req_get(self, url: str, header: dict, data: dict) -> requests.Response:
    return requests.get(url=url, headers=header)

  def __req_put(self, url: str, header: dict, data: dict) -> requests.Response:
    return requests.put(url=url, headers=header, json=data)

  def __req_patch(self, url: str, header: dict, data: dict) -> requests.Response:
    return requests.patch(url=url, headers=header, json=data)

  def __req_delete(self, url: str, header: dict, data: dict) -> requests.Response:
    return requests.delete(url=url, headers=header)
  ##      ##

  ## FORM ##
  def __req_post_form(self, url: str, header: dict, data: str, files: dict) -> requests.Response:
    return requests.post(url=url, headers=header, data=data, files=files)

  def __req_put_form(self, url: str, header: dict, data: str, files: dict) -> requests.Response:
    return requests.put(url=url, headers=header, data=data, files=files)

  def __req_patch_form(self, url: str, header: dict, data: str, files: dict) -> requests.Response:
    return requests.patch(url=url, headers=header, data=data, files=files)
  ##      ##

  async def add_request(self, request_info: RequestInformation) -> requests.Response | None:
    if request_info.request_url == "---":
      return

    request_id = uuid.uuid4()
    request_info.request_id = request_id

    await self.request_queue.put(request_info)
    while not request_id in self.responce_data:
      await asyncio.sleep(0.001)
    responce = self.responce_data.pop(request_id)
    if responce.status_code >= 400:
      self.logger.warning(f"Request error, code: {responce.status_code}")
      self.logger.debug(responce.json())
    return responce

  async def __worker_request(self):
    try:
      self.logger.info("Task started | name: worker=http_requestor")
      while True:
        request_informations = await self.request_queue.get()

        if "form" in request_informations.request_type:
          header = self.__header(self.__REQUEST_HEADER_CONTENT_TYPE_FORM, request_informations.request_need_token)
          responce = await asyncio.to_thread(self.request_functions_form[request_informations.request_type], request_informations.request_url, header, request_informations.request_body, request_informations.request_files)
        else:
          header = self.__header(self.__REQUEST_HEADER_CONTENT_TYPE_JSON, request_informations.request_need_token)
          responce = await asyncio.to_thread(self.request_functions[request_informations.request_type], request_informations.request_url, header, request_informations.request_body)

        self.logger.debug(f"Send request | type: {request_informations.request_type}, url: {request_informations.request_url}")

        self.responce_data[request_informations.request_id] = responce

        self.logger.debug(f"Complete request | code: {responce.status_code}")

        if 200 <= responce.status_code < 300: 
          request_rate_limit = responce.headers.get(self.__RESPONCE_HEADER_RATELIMIT)

          # TODO レート取得できなかったときのフィルターが皆無だから要修正
          if "/gateway" in request_informations.request_url:
            request_rate_limit = 1
          elif int(request_rate_limit) == 0:      # type: ignore
            wait_time = responce.headers.get(self.__RESPONCE_HEADER_RATELIMIT_WAITTIME)
            self.logger.debug(f"Rate limit -> wait | time: {wait_time}")
            await asyncio.sleep(float(wait_time)) # type: ignore

        self.request_queue.task_done()

    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"request worker error | reason: {str(e)}")

  async def request_worker_start(self):
    self.__task_request_worker = asyncio.create_task(self.__worker_request())

  async def request_worker_stop(self):
    if self.__task_request_worker:
      try:
        self.__task_request_worker.cancel()
        await self.__task_request_worker
      except:
        pass
      finally:
        self.logger.info("Task stopped | name: worker=http_requestor")