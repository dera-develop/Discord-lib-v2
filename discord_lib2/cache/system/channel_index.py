class ChannelIndex:
  def __init__(self) -> None:
    self.__index = {}

  def add(self, channel_id: str, guild_id: str):
    self.__index[channel_id] = guild_id

  def delete(self, channel_id: str):
    if channel_id in self.__index:
      self.__index.pop(channel_id)

  def get(self, channel_id: str):
    return self.__index.get(channel_id)