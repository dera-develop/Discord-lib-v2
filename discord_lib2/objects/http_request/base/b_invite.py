from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base

snowflake = str
image_data = str
ISO8601timestamp = str

@dataclass
class __InviteBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/invites/<invite.code>"

@dataclass
class GetInvite(__InviteBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class DeleteInvite(__InviteBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "delete"

@dataclass
class GetTargetUsers(__InviteBase):
  req_url:  ClassVar[str] = "/target-users"
  req_type: ClassVar[str] = "get"

@dataclass
class UpdateTargetUsers(__InviteBase):
  req_url:  ClassVar[str] = "/target-users"
  req_type: ClassVar[str] = "put"

  target_user_file: str

@dataclass
class GetTargetUsersJobStatus(__InviteBase):
  req_url:  ClassVar[str] = "/target-users/job-status"
  req_type: ClassVar[str] = "get"