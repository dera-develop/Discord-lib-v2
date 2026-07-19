import json

from discord_lib2.Network.gateway import structure_creator

snowflake = str

class Identify:
  """
  Identify  
  op: 2

  :param bot_token: Bot token
  :param intents: Bot intents
  :param prp_os: Using OS name | Ex) Linux
  """
  OP = 2

  def __init__(self, bot_token: str, intents: int, prp_os: str) -> None:
    self.identify_dict = {
      "op": self.OP,
      "d": {
        "token": bot_token,
        "intents": intents,
        "properties": {
          "os": prp_os,
          "browser": "discord_lib2",
          "device": "discord_lib2"
        }
      }
    }
  
  def set_compress(self, compress: bool) -> None:
    self.identify_dict["d"]["compress"] = compress
  
  def set_large_threshold(self, large_threshold: int) -> None:
    self.identify_dict["d"]["large_threshold"] = large_threshold
  
  def set_shard(self, shard: list) -> None:
    self.identify_dict["d"]["shard"] = shard

  def set_presence(self, presence: structure_creator.Presence) -> None:
    self.identify_dict["d"]["presence"] = presence
  
  def get(self) -> str:
    return json.dumps(self.identify_dict)

class Resume:
  """
  Resume  
  op: 6
  """
  OP = 6

  def __init__(self, session_token: str, session_id: str, last_seq_number: int | None) -> None:
    self.resume_dict = {
      "op": self.OP,
      "d": {
        "token": session_token,
        "session_id": session_id,
        "seq": last_seq_number
      }
    }

  def get(self) -> str:
    return json.dumps(self.resume_dict)

class Heartbeat:
  """
  Heartbeat  
  op: 1
  """
  OP = 1

  def __init__(self, last_seq_number) -> None:
    self.heartbeat_dict = {
      "op": self.OP,
      "d": last_seq_number
    }
  
  def get(self) -> str:
    return  json.dumps(self.heartbeat_dict)

class UpdateVoiceState:
  """
  Update voice state
  op: 4

  :param guild_id: Target guild id
  :param channel_id: Target channel id | if 'None', vcch disconnected.
  """
  OP = 4

  def __init__(self, guild_id: snowflake, channel_id: snowflake | None, self_mute: bool, self_deaf: bool) -> None:
    self.update_voice_state_dict = {
      "op": self.OP,
      "d": {
        "guild_id": guild_id,
        "channel_id": channel_id,
        "self_mute": self_mute,
        "self_deaf": self_deaf
      }
    }

  def get(self) -> str:
    return json.dumps(self.update_voice_state_dict)
  
class UpdatePresence:
  """
  Update presence
  op: 3

  :param presence: objects.Presence class object
  """
  def __init__(self, presence: structure_creator.Presence) -> None:
    self.update_presence_dict = {
      "op": 3,
      "d": presence
    }

  def get(self) -> str:
    return json.dumps(self.update_presence_dict)