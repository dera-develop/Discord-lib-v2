from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.logger import Logger

class UserEventResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, logger: Logger) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.logger = logger.get_child("GUE")
    
class UserTerminalCommandResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, logger: Logger) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.logger = logger.get_child("TUC")