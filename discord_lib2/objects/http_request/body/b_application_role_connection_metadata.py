from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

snowflake = str

@dataclass
class __ARCMBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications/<application.id>/role-connections/metadata"

@dataclass
class ApplicationRoleConnectionMetadata:
  T_INTEGER_LESS_THAN_OR_EQUAL: ClassVar[int] = 1
  T_INTEGER_GREATER_THAN_OR_EQUAL: ClassVar[int] = 2
  T_INTEGER_EQUAL: ClassVar[int] = 3
  T_INTEGER_NOT_EQUAL: ClassVar[int] = 4
  T_DATETIME_LESS_THAN_OR_EQUAL: ClassVar[int] = 5
  T_DATETIME_GREATER_THAN_OR_EQUAL: ClassVar[int] = 6
  T_BOOLEAN_EQUAL: ClassVar[int] = 7
  T_BOOLEAN_NOT_EQUAL: ClassVar[int] = 8

  type: int
  key: str
  name: str
  description: str
  name_localizations: dict | Exclude = Exclude()
  description_localizations: dict | Exclude = Exclude()


@dataclass
class GetApplicationRoleConnectionMetadataRecords(__ARCMBase):
  req_type: ClassVar[str] = "get"

@dataclass
class UpdateApplicationRoleConnectionMetadataRecords(__ARCMBase):
  req_type: ClassVar[str] = "put"