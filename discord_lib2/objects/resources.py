from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.logger import Logger
from discord_lib2.exception_catcher2 import ExceptionCatcher2

class UserEventResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, logger: Logger, exception_catcher: ExceptionCatcher2) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.logger = logger.get_child("UserEvent")
    self.__exception_catcher = exception_catcher

  async def stop_bot(self):
    await self.__exception_catcher.set_v(ExceptionCatcher2.STOP, 1000, "user event shutdown")
    
class UserTerminalCommandResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, logger: Logger, exception_catcher: ExceptionCatcher2) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.logger = logger.get_child("TermCom")
    self.__exception_catcher = exception_catcher

  async def stop_bot(self):
    await self.__exception_catcher.set_v(ExceptionCatcher2.STOP, 1000, "user terminal command shutdown")
    
class ApplicationCommandResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, logger: Logger, exception_catcher: ExceptionCatcher2) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.logger = logger.get_child("AppCom")
    self.__exception_catcher = exception_catcher

  async def stop_bot(self):
    await self.__exception_catcher.set_v(ExceptionCatcher2.STOP, 1000, "application command shutdown")