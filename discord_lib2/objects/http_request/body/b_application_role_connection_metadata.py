from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.http_request.format_checker import format_checker, PayloadFormatError
from discord_lib2.objects import locales

snowflake = str
EXCLUDE = Exclude()

ARCMT_INTEGER_LESS_THAN_OR_EQUAL = 1
ARCMT_INTEGER_GREATER_THAN_OR_EQUAL = 2
ARCMT_INTEGER_EQUAL = 3
ARCMT_INTEGER_NOT_EQUAL = 4
ARCMT_DATETIME_LESS_THAN_OR_EQUAL = 5
ARCMT_DATETIME_GREATER_THAN_OR_EQUAL = 6
ARCMT_BOOLEAN_EQUAL = 7
ARCMT_BOOLEAN_NOT_EQUAL = 8

# format check
FC_APPLICATION_ROLE_CONNECTION_METADATA_TYPE = (
  ARCMT_INTEGER_LESS_THAN_OR_EQUAL, ARCMT_INTEGER_GREATER_THAN_OR_EQUAL, ARCMT_INTEGER_EQUAL, ARCMT_INTEGER_NOT_EQUAL,
  ARCMT_DATETIME_LESS_THAN_OR_EQUAL, ARCMT_DATETIME_GREATER_THAN_OR_EQUAL, ARCMT_BOOLEAN_EQUAL, ARCMT_BOOLEAN_NOT_EQUAL
)

@dataclass
class __ARCMBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/applications/<application.id>/role-connections/metadata"

@dataclass
class ApplicationRoleConnectionMetadata(Base):
  type: int
  key: str
  name: str
  description: str
  name_localizations: dict[str, str] | Exclude=EXCLUDE
  description_localizations: dict[str, str] | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=FC_APPLICATION_ROLE_CONNECTION_METADATA_TYPE)
    # key
    format_checker(self.key, "key", 1, 50)
    for c in self.key:
      if not ("a" <= c <= "z" or "0" <= c <= "9" or c == "_"):
        raise PayloadFormatError("key", "must be `a-z`, `0-9` or `_` characters")
    # name
    format_checker(self.name, "name", 1, 100)
    if isinstance(self.name_localizations, dict):
      for key, value in self.name_localizations.items():
        if not key in locales.LOCALES:
          raise PayloadFormatError("name_localizations", f"unknown locale: {key}")
        format_checker(value, f"name_localizations.{key}", 1, 100)
    # description
    format_checker(self.description, "description", 1, 100)
    if isinstance(self.description_localizations, dict):
      for key, value in self.description_localizations.items():
        if not key in locales.LOCALES:
          raise PayloadFormatError("description_localizations", f"unknown locale: {key}")
        format_checker(value, f"description_localizations.{key}", 1, 100)
    return super().format_check()

@dataclass
class GetApplicationRoleConnectionMetadataRecords(__ARCMBase):
  req_type: ClassVar[str] = "get"

@dataclass
class UpdateApplicationRoleConnectionMetadataRecords(__ARCMBase):
  req_type: ClassVar[str] = "put"