snowflake = str

class Activity:
  """
  Activity object
  """
  # timestamps object
  def timestamps(self, unix_timestamp_start: int, unix_timestamp_end: int) -> dict:
    return {
      "start": unix_timestamp_start,
      "end": unix_timestamp_end
    }

  # emoji object
  def emoji(self, name: str, id: snowflake, animated: bool) -> dict:
    return {
      "name": name,
      "id": id,
      "animated": animated
    }

  # party object
  def party(self, id: str, size: list[int]) -> dict:
    return {
      "id": id,
      "size": size
    }

  # secrets object
  def secrets(self, join: str, spectate: str, match: str) -> dict:
    return {
      "join": join,
      "spectate": spectate,
      "match": match
    }

  # flags object
  FLAGS__INSTANCE = 1
  FLAGS__JOIN = 2
  FLAGS__SPECTATE = 4
  FLAGS__JOIN_REQUEST = 8
  FLAGS__SYNC = 16
  FLAGS__PLAY = 32
  FLAGS__PARTY_PRIVACY_FRIENDS = 64
  FLAGS__PARTY_PRIVACY_VOICE_CHANNEL = 128
  FLAGS__EMBEDDED = 256

  def flags(self, *flags: int) -> int:
    flag_int = 0
    for flag in flags:
      flag_int += flag
    return flag_int

  # button object
  def button(self, label: str, url: str):
    return {
      "label": label,
      "url": url
    }

  # - # - # - # - # - # - # - #

  ACTIVITY_TYPE__PLAYING   = 0
  ACTIVITY_TYPE__STREAMING = 1
  ACTIVITY_TYPE__LISTENING = 2
  ACTIVITY_TYPE__WATCHING  = 3
  ACTIVITY_TYPE__CUSTOM    = 4
  ACTIVITY_TYPE__COMPETING = 5

  STATUS_DISPLAY_TYPE__NAME    = 0
  STATUS_DISPLAY_TYPE__STATE   = 1
  STATUS_DISPLAY_TYPE__DETAILS = 2

  def __init__(self) -> None:
    self.activity_dict = {}

  def set_name(self, activity_name: str) -> None:
    self.activity_dict["name"] = activity_name

  def set_type(self, activity_type: int) -> None:
    self.activity_dict["type"] = activity_type

  def set_url(self, streaming_url: str) -> None:
    self.activity_dict["url"] = streaming_url

  def set_created_at(self, timestamps_object: dict) -> None:
    self.activity_dict["created_at"] = timestamps_object

  def set_application_id(self, application_id: snowflake) -> None:
    self.activity_dict["application_id"] = application_id

  def set_status_display_type(self, status_display_type: int) -> None:
    self.activity_dict["status_display_type"] = status_display_type

  def set_details(self, details: str) -> None:
    self.activity_dict["details"] = details

  def set_details_url(self, details_url: str) -> None:
    self.activity_dict["details_url"] = details_url

  def set_state(self, state: str) -> None:
    self.activity_dict["state"] = state

  def set_state_url(self, state_url: str) -> None:
    self.activity_dict["state_url"] = state_url

  def set_emoji(self, emoji_object: dict) -> None:
    self.activity_dict["emoji"] = emoji_object

  def set_party(self, party_object: dict) -> None:
    self.activity_dict["party"] = party_object

  def set_secrets(self, secrets_object: dict) -> None:
    self.activity_dict["secrets_object"] = secrets_object

  def set_instance(self, instance: bool) -> None:
    self.activity_dict["instance"] = instance

  def add_buttons(self, buttons: dict) -> None:
    if not "buttons" in self.activity_dict:
      self.activity_dict["buttons"] = [buttons]
    else:
      self.activity_dict["buttons"].append(buttons)

  def get(self) -> dict:
    return self.activity_dict

class Presence:
  """
  Presence object
  """
  ONLINE        = "online"
  DONT_DISTURB  = "dnd"
  AFK           = "idle"
  SHOW_OFFLINE  = "invisible"
  OFFLINE       = "offline"

  def __init__(self) -> None:
    self.presence_dict = {}

  def set_since(self, since: int) -> None:
    self.presence_dict["since"] = since

  def set_activities(self, activities: Activity) -> None:
    self.presence_dict["activities"] = activities

  def set_status(self, status: str) -> None:
    self.presence_dict["status"] = status

  def set_afk(self, afk: bool) -> None:
    self.presence_dict["afk"] = afk

  def get(self) -> dict:
    return self.presence_dict

class User:
  def __init__(self) -> None:
    pass