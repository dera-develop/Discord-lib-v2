from discord_lib2.Network.gateway.websocket import WebsocketController

from discord_lib2.objects.gateway import request_payload

snowflake = str

class GatewayRequest:
  def __init__(self, gateway_controller: WebsocketController) -> None:
    self.__gateway = gateway_controller

  async def request_guild_member(self, payload: request_payload.RequestGuildMembers) -> None:
    await self.__gateway.send(payload.get())

  async def request_soundboard_sounds(self, payload: request_payload.RequestSoundboardSounds) -> None:
    await self.__gateway.send(payload.get())

  async def request_channel_info(self, payload: request_payload.RequestChannelInfo) -> None:
    await self.__gateway.send(payload.get())