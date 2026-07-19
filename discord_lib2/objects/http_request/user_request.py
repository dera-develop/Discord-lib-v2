from discord_lib2.Network.http_request.http import HttpRequestController, RequestInformation
from discord_lib2.Network.http_request.request_loader import RequestLoader


class HttpRequest:
  def __init__(self, http_request_controller: HttpRequestController, request_loader: RequestLoader) -> None:
    self.__requestor = http_request_controller
    self.load_request = request_loader.request_load

  async def request(self, request_info: RequestInformation):
    return await self.__requestor.add_request(request_info)