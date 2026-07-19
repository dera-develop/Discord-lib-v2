from discord_lib2.cache.user import DataCacheVault
from discord_lib2.cache.onetime import OnetimeCacheVault
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest

class UserEventResources:
  def __init__(self, gateway: GatewayRequest, http_api: HttpRequest, data_cache: DataCacheVault, onetime_cache: OnetimeCacheVault) -> None:
    self.gateway = gateway
    self.http_api = http_api
    self.cache = data_cache
    self.cache_onetime = onetime_cache