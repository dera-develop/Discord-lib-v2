from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base

@dataclass
class __ApplicationCommandBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications/<application.id>"

@dataclass
class GetGlobalApplicationCommands(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGlobalApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands"
  req_type: ClassVar[str] = "post"

  data: dict
  def get(self) -> dict | list:
    return self.data

@dataclass
class GetGlobalApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands/<command.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class EditGlobalApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands/<command.id>"
  req_type: ClassVar[str] = "patch"

  data: dict
  def get(self) -> dict | list:
    return self.data

@dataclass
class DeleteGlobalApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands/<command.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkOverwriteGlobalApplicationCommands(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/commands"
  req_type: ClassVar[str] = "put"

@dataclass
class GetGuildApplicationCommands(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands"
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands"
  req_type: ClassVar[str] = "post"

  data: dict
  def get(self) -> dict | list:
    return self.data

@dataclass
class GetGuildApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/<command.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class EditGuildApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/<command.id>"
  req_type: ClassVar[str] = "patch"

  data: dict
  def get(self) -> dict | list:
    return self.data

@dataclass
class DeleteGuildApplicationCommand(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/<command.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class BulkOverwriteGuildApplicationCommands(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands"
  req_type: ClassVar[str] = "put"

@dataclass
class GetGuildApplicationCommandPermissions(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/permissions"
  req_type: ClassVar[str] = "get"

@dataclass
class GetApplicationCommandPermissions(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/<command.id>/permissions"
  req_type: ClassVar[str] = "get"

@dataclass
class EditApplicationCommandPermissions(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/<jcommand.id>/permissions"
  req_type: ClassVar[str] = "put"

@dataclass
class BatchEditApplicationCommandPermissions(__ApplicationCommandBase):
  req_url: ClassVar[str] = "/guilds/<guild.id>/commands/permissions"
  req_type: ClassVar[str] = "put"