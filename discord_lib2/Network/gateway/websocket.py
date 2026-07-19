import websockets
import asyncio
import json
import zlib
from typing import ClassVar

from discord_lib2.logger import Logger
from discord_lib2.exception_catcher import ExceptionCatcher
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.Network.gateway import event_creators

class WebsocketController:
  URL_GATEWAY_QUERY: ClassVar[str]  = "?v=10&encoding=json&compress=zlib-stream"

  OP_DISPATCH: ClassVar[int] = 0
  OP_HEARTBEAT: ClassVar[int] = 1
  OP_IDENTIFY: ClassVar[int] = 2
  OP_PRESENCE_UPDATE: ClassVar[int] = 3
  OP_VOICE_STATE_UPDATE: ClassVar[int] = 4
  OP_RESUME: ClassVar[int] = 6
  OP_RECONNECT: ClassVar[int] = 7
  OP_INVALID_SESSION: ClassVar[int] = 9
  OP_HELLO: ClassVar[int] = 10
  OP_HEARTBEAT_ACK: ClassVar[int] = 11

  RATELIMIT_GATEWAY_SEND_PER_MIN: ClassVar[int] = 120
  counter_send_event = 0

  RECVED_CHECK_STRING: ClassVar[bytes] = b"\x00\x00\xff\xff"

  def __init__(self,logger: Logger, system_cache_vault: SystemCacheVault, exception_catcher: ExceptionCatcher):
    self.logger = logger.get_child("WSC")
    self.system_cache_vault = system_cache_vault
    self.exception_catcher = exception_catcher
    self.event_queue_send = asyncio.Queue()
    self.event_queue_recv = asyncio.Queue()
    self.event_queue_dispatch = asyncio.Queue()

    self.system_cache_vault.gateway.heartbeat_interval = -1

    self.op_event_functions = {
      self.OP_DISPATCH: self.__op_event_dispatch,
      self.OP_RECONNECT: self.__op_event_reconnect,
      self.OP_INVALID_SESSION: self.__op_event_invalid_session,
      self.OP_HELLO: self.__op_event_hello,
      self.OP_HEARTBEAT_ACK: self.__op_event_heartbeat_ack
    }

  async def websocket_connect(self) -> bool:
    self.logger.info(f"Websocket connect | target: {f"{self.system_cache_vault.gateway.gateway_url}/{self.URL_GATEWAY_QUERY}"}")
    try:
      self.websocket_connect_object = await websockets.connect(uri=f"{self.system_cache_vault.gateway.gateway_url}/{self.URL_GATEWAY_QUERY}")
      await self.__task_runner()
      self.logger.info(f"connected.")

    except Exception as e:
      self.logger.exception(f"Failed connect websocket | reason: {str(e)}")
      return False
    
    return True
  
  async def websocket_disconnect(self, code: int=1000, reason: str="system shutdown", only_task_stop: bool=False):
    await self.__task_stopper()
    if not only_task_stop:
      self.logger.info(f"Websocket disconnect | code: {code}, reason: {reason}")
      await self.websocket_connect_object.close(code=code, reason=reason)

  async def __task_runner(self):
    self.__task_sendrate_controller = asyncio.create_task(self.__worker_sendrate_controller())
    self.__task_send_worker   = asyncio.create_task(self.__worker_send())
    self.__task_recv_worker   = asyncio.create_task(self.__worker_recv())
    self.__task_event_trigger = asyncio.create_task(self.__worker_event_trigger())
    self.__task_heartbeat     = asyncio.create_task(self.__worker_heartbeat())

  async def __task_stopper(self):
    if self.__task_send_worker:
      try:
        self.__task_send_worker.cancel()
        await self.__task_send_worker
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | name: worker=send")

    if self.__task_recv_worker:
      try:
        self.__task_recv_worker.cancel()
        await self.__task_recv_worker
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | name: worker=recv")

    if self.__task_sendrate_controller:
      try:
        self.__task_sendrate_controller.cancel()
        await self.__task_sendrate_controller
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | name: worker=send_rate_controller")

    if self.__task_event_trigger:
      try:
        self.__task_event_trigger.cancel()
        await self.__task_event_trigger
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | name: worker=event_trigger")

    if self.__task_heartbeat:
      try:
        self.__task_heartbeat.cancel()
        await self.__task_heartbeat
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | name: worker=heartbeat")

  # # # # # # # # # # # # # # # # # # # # # # # # # #
  # Worker
  # # # # # # # # # # # # # # # # # # # # # # # # # #

  # event send
  async def __worker_send(self):
    try:
      self.logger.info(f"Task started | name: worker=send")
      while True:
        if self.counter_send_event < self.RATELIMIT_GATEWAY_SEND_PER_MIN:
          self.counter_send_event += 1
          send_data = await self.event_queue_send.get()
          await self.websocket_connect_object.send(send_data)
          self.event_queue_send.task_done()
        else:
          await asyncio.sleep(0.2)

    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  # event receive
  async def __worker_recv(self):
    try:
      self.logger.info(f"Task started | name: worker=recv")
      recv_buf = bytearray()
      zlib_decompressor = zlib.decompressobj()
      json_decompressor = json.JSONDecoder()
      while True:
        while True:
          recv_raw = await self.websocket_connect_object.recv()
          if isinstance(recv_raw, bytes):
            recv_buf.extend(recv_raw)
            if len(recv_buf) >= 4 and recv_buf[-4:] == self.RECVED_CHECK_STRING:
              json_raw = zlib_decompressor.decompress(recv_buf).decode("utf-8")
              recv_buf.clear()
              break
        pos = 0
        length = len(json_raw)
        while pos < length:
          json_data, index = json_decompressor.raw_decode(json_raw[pos:])
          await self.event_queue_recv.put(json_data)
          pos += index

    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  # event trigger
  async def __worker_event_trigger(self):
    try:
      self.logger.info(f"Task started | name: worker=event_trigger")
      while True:
        event_payload = await self.event_queue_recv.get()
        op = event_payload.get("op")
        d  = event_payload.get("d")
        t  = event_payload.get("t")
        s  = event_payload.get("s")

        self.logger.debug(f"received event | op: {op}, t: {t}, s: {s}")
        self.system_cache_vault.gateway.last_recv_seq = s
        await self.op_event_functions[op](d=d, t=t)

    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  # event send rate controller
  async def __worker_sendrate_controller(self):
    try:
      self.logger.info(f"Task started | name: worker=rate_controller")
      while True:
        await asyncio.sleep(60)
        self.counter_send_event = 0
    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  # heartbeat
  async def __worker_heartbeat(self):
    try:
      self.logger.info(f"Task started | name: worker=heartbeat")
      self.system_cache_vault.gateway.heartbeat_recved = 0
      self.system_cache_vault.gateway.heartbeat_sended = 0
      while True:
        if self.system_cache_vault.gateway.heartbeat_interval == -1:
          await asyncio.sleep(0.1)
          continue
        await asyncio.sleep(self.system_cache_vault.gateway.heartbeat_interval / 1000)
        if self.system_cache_vault.gateway.heartbeat_recved == self.system_cache_vault.gateway.heartbeat_sended:
          event = event_creators.Heartbeat(self.system_cache_vault.gateway.last_recv_seq)
          await self.send(event.get())
          self.system_cache_vault.gateway.heartbeat_sended += 1
        else:
          self.logger.error(f"counter error | send: {self.system_cache_vault.gateway.heartbeat_sended}, recv: {self.system_cache_vault.gateway.heartbeat_recved}")
          self.exception_catcher.set_v(self.exception_catcher.RECONNECT, 4000, "auto_reconnect")
    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"Application error | reason: {str(e)}")

  # # # # # # # # # # # # # # # # # # # # # # # # # #

  async def send(self, send_json: str):
    await self.event_queue_send.put(send_json)

  async def get_event_queue(self) -> str:
    return await self.event_queue_dispatch.get()

  # # # # # # # # # # # # # # # # # # # # # # # # # #
  # op event task functions
  # # # # # # # # # # # # # # # # # # # # # # # # # #

  def reconnect(self, close_code: int=1000, close_reason: str="auto reconnect"):
    self.exception_catcher.set_v(self.exception_catcher.RECONNECT, close_code, close_reason)

  def stconnect(self, close_code: int=1000, close_reason: str="auto shutdown"):
    self.exception_catcher.set_v(self.exception_catcher.STOP, close_code, close_reason)

  async def __op_event_dispatch(self, d, t):
    await self.event_queue_dispatch.put(json.dumps({"t": t, "d": d}))

  async def __op_event_reconnect(self, d, t):
    self.reconnect()

  async def __op_event_invalid_session(self, d, t):
    can_resume = d
    if can_resume:
      self.reconnect()
    else:
      self.stconnect()

  async def __op_event_hello(self, d, t):
    interval = d.get("heartbeat_interval")
    self.logger.debug(f"set heartbeat interval: {interval}")
    self.system_cache_vault.gateway.heartbeat_interval = interval
    
    # first connection
    if self.system_cache_vault.resume.reconnect_gateway_url == "":
      event = event_creators.Identify(self.system_cache_vault.bot_token, self.system_cache_vault.bot_intents, self.system_cache_vault.os_type)
      if self.system_cache_vault.compress is not None:
        event.set_compress(self.system_cache_vault.compress)
      if self.system_cache_vault.large_threshold is not None:
        event.set_large_threshold(self.system_cache_vault.large_threshold)
      if self.system_cache_vault.shard is not None:
        event.set_shard(self.system_cache_vault.shard)
      if self.system_cache_vault.presence is not None:
        event.set_presence(self.system_cache_vault.presence)
      await self.send(event.get())

    # reconnection
    else:
      event = event_creators.Resume(self.system_cache_vault.bot_token, self.system_cache_vault.resume.session_id, self.system_cache_vault.gateway.last_recv_seq)
      await self.send(event.get())

  async def __op_event_heartbeat_ack(self, d, t):
    self.system_cache_vault.gateway.heartbeat_recved += 1