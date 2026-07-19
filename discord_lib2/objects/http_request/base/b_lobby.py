from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude

snowflake = str

@dataclass
class __LobbyBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/lobbies"

MF_CANLINKLOBBY = 1 << 0

@dataclass
class LobbyMember:
  id: snowflake
  metadata: dict | None | Exclude = Exclude()
  flags: int | Exclude = Exclude()

@dataclass
class CreateLobby(__LobbyBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  metadata: dict | None | Exclude = Exclude()
  members: list[LobbyMember] | Exclude = Exclude()
  idle_timeout_seconds: int | Exclude = Exclude()

  def format_check(self, filtered_dict) -> None:
    if filtered_dict.get("metadata") is not None:
      if len(filtered_dict.get("metadata")) > 1000:
        raise body_base.PayloadFormatError("'metadata': The length must be 1000 or less.")
    
    if filtered_dict.get("members") is not None:
      if filtered_dict.get("members").get("metadata") is not None:
        if len(filtered_dict.get("members").get("metadata")) > 1000:
          raise body_base.PayloadFormatError("'members/metadata': The length must be 1000 or less.")
        
@dataclass
class CreateorJoinLobby(__LobbyBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "put"

  secret: str
  idle_timeout_seconds: int | Exclude = Exclude()
  lobby_metadata: dict | None | Exclude = Exclude()
  member_metadata: dict | None | Exclude = Exclude()

  def format_check(self, filtered_dict) -> None:
    if len(filtered_dict.get("secret")) > 250:
      raise body_base.PayloadFormatError("'secret': It must be 250 characters or less.")
    
    if filtered_dict.get("idle_timeout_seconds") is not None:
      if not 5 <= filtered_dict.get("idle_timeout_seconds") <= 604800:
        raise body_base.PayloadFormatError("'idle_timeout_seconds': It must be between 5 and 604800.")

    if filtered_dict.get("lobby_metadata") is not None:
      if len(filtered_dict.get("lobby_metadata")) > 1000:
        raise body_base.PayloadFormatError("'lobby_metadata': The length must be 1000 or less.")

    if filtered_dict.get("member_metadata") is not None:
      if len(filtered_dict.get("member_metadata")) > 1000:
        raise body_base.PayloadFormatError("'memter_metadata': The length must be 1000 or less.")
      
@dataclass
class GetLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "patch"

  metadata: dict | None | Exclude = Exclude()
  members: list[LobbyMember] | Exclude = Exclude()
  idle_timeout_seconds: int | Exclude = Exclude()

  def format_check(self, filtered_dict):
    if filtered_dict.get("idle_timeout_seconds") is not None:
      if not 5 <= filtered_dict.get("idle_timeout_seconds") <= 604800:
        raise body_base.PayloadFormatError("'idle_timeout_seconds': It must be between 5 and 604800.")

    if filtered_dict.get("metadata") is not None:
      if len(filtered_dict.get("metadata")) > 1000:
        raise body_base.PayloadFormatError("'metadata': The length must be 1000 or less.")
      
@dataclass
class DeleteLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class AddaMembertoaLobby(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/<user.id>"
  req_type: ClassVar[str] = "put"

  metadata: dict | None | Exclude = Exclude()
  flags: int | Exclude = Exclude()

  def format_check(self, filtered_dict):
    if filtered_dict.get("metadata") is not None:
      if len(filtered_dict.get("metadata")) > 1000:
        raise body_base.PayloadFormatError("'metadata': The length must be 1000 or less.")
      
@dataclass
class BulkUpdateLobbyMembers(__LobbyBase):
  req_url:  ClassVar[str] = "/<lobby.id>/members/bulk"
  req_type: ClassVar[str] = "post"

  id: snowflake
  metadata: dict | None | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  remove_member: bool | Exclude = Exclude()

  def format_check(self, filtered_dict):
    if filtered_dict.get("metadata") is not None:
      if len(filtered_dict.get("metadata")) > 1000:
        raise body_base.PayloadFormatError("'metadata': The length must be 1000 or less.")

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
  metadata: dict | None | Exclude = Exclude()
  flags: int | Exclude = Exclude()

  def format_check(self, filtered_dict):
    if filtered_dict.get("metadata") is not None:
      if len(filtered_dict.get("metadata")) > 1000:
        raise body_base.PayloadFormatError("'metadata': The length must be 1000 or less.")

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