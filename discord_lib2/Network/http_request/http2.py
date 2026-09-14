from typing import Any, Callable, Coroutine

import aiohttp
import asyncio
import uuid
import json

from multidict import CIMultiDictProxy, CIMultiDict

from discord_lib2.logger import Logger
from discord_lib2.Network.http_request.request_loader import RequestInformation
from discord_lib2.cache.system import system

class RequestFailedError(Exception):
  def __init__(self, name: str) -> None:
    super().__init__(name)

class RequestQueue(asyncio.Queue):
  async def put(self, item: RequestInformation) -> None:
    return await super().put(item)
  async def get(self) -> RequestInformation:
    return await super().get()

class RequestResponse:
  def __init__(self) -> None:
    self.status_code: int = -1
    self.headers: CIMultiDictProxy[str] = CIMultiDictProxy(CIMultiDict())
    self.reason: str | None = None
    self.ok: bool = False
    self.json: Any = None
    self.text: str = ""

  async def _set_datas(self, res: aiohttp.ClientResponse):
    self.status_code = res.status
    self.headers = res.headers
    self.reason = res.reason
    self.ok = res.ok
    res_body = await res.read()
    try:
      self.text = res_body.decode(res.get_encoding() or "utf-8", errors="replace")
    except:
      self.text = ""
    try:
      self.json = json.loads(res_body)
    except:
      self.json = {}

class HttpRequestController:
  __task_request_worker = None
  __RESPONCE_HEADER_RATELIMIT = "X-RateLimit-Remaining"
  __RESPONCE_HEADER_RATELIMIT_WAITTIME = "X-RateLimit-Reset-After"

  __REQUEST_HEADER_CONTENT_TYPE_JSON = "application/json"
  __REQUEST_HEADER_CONTENT_TYPE_FORM = "multipart/form-data"

  def __init__(self, system_cache: system.SystemCacheVault, logger: Logger) -> None:
    self.logger = logger.get_child("HRC")
    self.system_cache_vault = system_cache

    self.request_queue = RequestQueue()
    self.response_datas: dict[uuid.UUID, RequestResponse | None] = {}

    self.req_json_functions: dict[str, Callable[..., Coroutine[Any, Any, RequestResponse]]] = {
      "post": self.__req_json_post,
      "get":  self.__req_json_get,
      "put":  self.__req_json_put,
      "patch":  self.__req_json_patch,
      "delete": self.__req_json_delete
    }
    self.req_form_functions: dict[str, Callable[..., Coroutine[Any, Any, RequestResponse]]] = {
      "post_form":  self.__req_form_post,
      "put_form":   self.__req_form_put,
      "patch_form": self.__req_form_patch
    }

  ## JSON ##
  async def __req_json_post(self, session: aiohttp.ClientSession, url: str, header: dict, json_data: dict) -> RequestResponse:
    async with session.post(url=url, headers=header, json=json_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_json_get(self, session: aiohttp.ClientSession, url: str, header: dict, json_data: dict) -> RequestResponse:
    async with session.get(url=url, headers=header) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_json_put(self, session: aiohttp.ClientSession, url: str, header: dict, json_data: dict) -> RequestResponse:
    async with session.put(url=url, headers=header, json=json_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_json_patch(self, session: aiohttp.ClientSession, url: str, header: dict, json_data: dict) -> RequestResponse:
    async with session.patch(url=url, headers=header, json=json_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_json_delete(self, session: aiohttp.ClientSession, url: str, header: dict, json_data: dict) -> RequestResponse:
    async with session.delete(url=url, headers=header) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos
  ##      ##

  ## FORM ##
  async def __req_form_post(self, session: aiohttp.ClientSession, url: str, header: dict, form_data: aiohttp.FormData) -> RequestResponse:
    async with session.post(url=url, headers=header, data=form_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_form_put(self, session: aiohttp.ClientSession, url: str, header: dict, form_data: aiohttp.FormData) -> RequestResponse:
    async with session.put(url=url, headers=header, data=form_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos

  async def __req_form_patch(self, session: aiohttp.ClientSession, url: str, header: dict, form_data: aiohttp.FormData) -> RequestResponse:
    async with session.patch(url=url, headers=header, data=form_data) as res:
      res_infos = RequestResponse()
      await res_infos._set_datas(res)
      return res_infos
  ##      ##

  def __get_header(self, content_type: str, enable_token: bool):
    header_base = {
      "User-Agent": f"DiscordBot (https://github.com/dera-develop/Discord-lib-v2), 2.0",
      "Content-Type": content_type
    }
    if content_type == self.__REQUEST_HEADER_CONTENT_TYPE_FORM:
      header_base.pop("Content-Type")
    if enable_token:
      header_base["Authorization"] = f"Bot {self.system_cache_vault.bot_token}"
    return header_base

  async def add_request(self, request_info: RequestInformation) -> RequestResponse:
    if request_info.request_url == "---":
      raise RequestFailedError("Failed load request informations")

    # set uuid
    while True:
      req_id = uuid.uuid4()
      if not (req_id in self.response_datas):
        break
      await asyncio.sleep(0.001)
    request_info.request_id = req_id

    # request
    await self.request_queue.put(request_info)

    # wait response
    while not req_id in self.response_datas:
      await asyncio.sleep(0.001)
    res = self.response_datas.pop(req_id)
    if res is None:
      raise RequestFailedError("Exception error")
    if res.status_code >= 400:
      self.logger.warning(f"Request error, code: {res.status_code}")
      self.logger.warning(res.json)
    return res

  async def __worker_request(self):
    self.logger.info("Task started | name: worker=http_requestor")
    async with aiohttp.ClientSession() as session:
      try:
        while True:
          req_infos = await self.request_queue.get()

          #####debug
          #self.logger.debug(f"Send request | type: {req_infos.request_type}, url: {req_infos.request_url}")
          #self.logger.debug(f"body   // {req_infos.request_body}")

          if "form" in req_infos.request_type:
            header = self.__get_header(self.__REQUEST_HEADER_CONTENT_TYPE_FORM, req_infos.request_need_token)
            try:
              res = await self.req_form_functions[req_infos.request_type](session, req_infos.request_url, header, req_infos.request_form)
            except asyncio.CancelledError:
              raise
            except Exception as e:
              self.logger.exception(f"request worker error | reason: {str(e)}")
              self.response_datas[req_infos.request_id] = None
              self.request_queue.task_done()
              continue
          else:
            header = self.__get_header(self.__REQUEST_HEADER_CONTENT_TYPE_JSON, req_infos.request_need_token)
            try:
              res = await self.req_json_functions[req_infos.request_type](session, req_infos.request_url, header, req_infos.request_body)
            except asyncio.CancelledError:
              raise
            except Exception as e:
              self.logger.exception(f"request worker error | reason: {str(e)}")
              self.response_datas[req_infos.request_id] = None
              self.request_queue.task_done()
              continue

          self.response_datas[req_infos.request_id] = res

          #####debug
          #self.logger.debug(f"Complete request | code: {res.status_code}")

          if 200 <= res.status_code < 300:
            request_rate_limit = res.headers.get(self.__RESPONCE_HEADER_RATELIMIT)

            #TODO
            try:
              if "/gateway" in req_infos.request_url:
                request_rate_limit = 1
              elif int(request_rate_limit) == 0:      # type: ignore
                wait_time = res.headers.get(self.__RESPONCE_HEADER_RATELIMIT_WAITTIME)
                self.logger.debug(f"Rate limit -> wait | time: {wait_time}")
                await asyncio.sleep(float(wait_time)) # type: ignore
            except Exception as e:
              self.logger.exception(f"response headers load error(rate_limit) | wait 10s | reason: {str(e)}")
              await asyncio.sleep(10)

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