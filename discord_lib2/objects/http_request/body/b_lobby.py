from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str

MF_CANLINKLOBBY = 1 << 0
EXCLUDE = Exclude()

@dataclass
class __LobbyBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/lobbies"

@dataclass
class LobbyMember(Base):
  id: snowflake
  metadata: dict | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  additional_name: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    format_checker(self.additional_name, "additional_name", 1, 80)
    return super().format_check()

@dataclass
class CreateLobby(__LobbyBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  metadata: dict | None | Exclude=EXCLUDE
  members: list[LobbyMember] | Exclude=EXCLUDE
  idle_timeout_seconds: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    format_checker(self.members, "members", 0, 25)
    format_checker(self.idle_timeout_seconds, "idle_timeout_seconds", 5, 604800)
    return super().format_check()
        
@dataclass
class CreateorJoinLobby(__LobbyBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "put"

  secret: str
  idle_timeout_seconds: int | Exclude=EXCLUDE
  lobby_metadata: dict | None | Exclude=EXCLUDE
  member_metadata: dict | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.secret, "secret", 0, 250)
    format_checker(self.idle_timeout_seconds, "idle_timeout_seconds", 5, 604800)
    format_checker(self.lobby_metadata, "lobby_metadata", 0, 1000)
    format_checker(self.member_metadata, "member_metadata", 0, 1000)
    return super().format_check()
      
@dataclass
class GetLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "patch"

  metadata: dict | None | Exclude=EXCLUDE
  members: list[LobbyMember] | Exclude=EXCLUDE
  idle_timeout_seconds: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    format_checker(self.members, "members", 0, 25)
    format_checker(self.idle_timeout_seconds, "idle_timeout_seconds", 5, 604800)
    return super().format_check()
      
@dataclass
class DeleteLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class AddaMembertoaLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/<user.id>"
  req_type: ClassVar[str] = "put"

  metadata: dict | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  additional_name: str | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    format_checker(self.additional_name, "additional_name", 1, 80)
    return super().format_check()
      
@dataclass
class BulkUpdateLobbyMembers(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/bulk"
  req_type: ClassVar[str] = "post"

  id: snowflake
  metadata: dict | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  additional_name: str | None | Exclude=EXCLUDE
  remove_member: bool | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    format_checker(self.additional_name, "additional_name", 1, 80)
    return super().format_check()

@dataclass
class RemoveaMemberfromaLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/<user.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class LeaveLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/@me"
  req_type: ClassVar[str] = "delete"

@dataclass
class LinkChanneltoLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/channel-linking"
  req_type: ClassVar[str] = "patch"

  channel_id: snowflake

@dataclass
class UnlinkChannelfromLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/channel-linking"
  req_type: ClassVar[str] = "patch"

@dataclass
class SendLobbyMessage(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/messages"
  req_type: ClassVar[str] = "post"

  content: str
  metadata: dict | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.metadata, "metadata", 0, 1000)
    return super().format_check()

@dataclass
class GetLobbyMessages(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/messages"
  req_type: ClassVar[str] = "get"

@dataclass
class UpdateLobbyMessageModerationMetadata(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id/messages/<message.id>/moderation-metadata"
  req_type: ClassVar[str] = "put"

  def __init__(self, moderation_dict: dict) -> None:
    self.args = moderation_dict

  def format_check(self) -> None:
    format_checker(self.args, "moderation_dict", 0, 5)
    for k, v in self.args.items():
      format_checker(k, f"moderation_dict.{k}", 0, 1024)
      format_checker(v, f"moderation_dict.{v}", 0, 2000)
    return super().format_check()
  
  def get(self):
    return self.args
  
@dataclass
class CreateLobbyChannelInviteforSelf(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/@me/invites"
  req_type: ClassVar[str] = "post"

@dataclass
class CreateLobbyChannelInviteforUser(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/<user.id>/invites"
  req_type: ClassVar[str] = "post"

  code: str