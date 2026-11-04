from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.http_request.body import b_application_role_connection_metadata

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
image_data = StopAsyncIteration
EXCLUDE = Exclude()

@dataclass
class __UserBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/users"

@dataclass
class AvatarDecorationData(Base):
  asset: str
  sku_id: snowflake

@dataclass
class Nameplate(Base):
  sku_id: snowflake
  asset: str
  label: str
  palette: str

@dataclass
class Collectibles(Base):
  nameplate: Nameplate

@dataclass
class User(Base):
  @dataclass
  class PrimaryGuild(Base):
    identity_guild_id: snowflake | None
    identity_enaabled: bool | None
    tag: str | None
    badge: str | None

  F_STAFF: ClassVar[int] = 1 << 0
  F_PARTNER: ClassVar[int] = 1 << 1
  F_HYPESQUAD: ClassVar[int] = 1 << 2
  F_BUG_HUNTER_LEVEL_1: ClassVar[int] = 1 << 3
  F_HYPESQUAD_ONLINE_HOUSE_1: ClassVar[int] = 1 << 6
  F_HYPESQUAD_ONLINE_HOUSE_2: ClassVar[int] = 1 << 7
  F_HYPESQUAD_ONLINE_HOUSE_3: ClassVar[int] = 1 << 8
  F_PREMIUM_EARLY_SUPPORTER: ClassVar[int] = 1 << 9
  F_TEAM_PSEUDO_USER: ClassVar[int] = 1 << 10
  F_BUG_HUNTER_LEVEL_2: ClassVar[int] = 1 << 14
  F_VERIFIED_BOT: ClassVar[int] = 1 << 16
  F_VERIFIED_DEVELOPER: ClassVar[int] = 1 << 17
  F_CERTIFIED_MODERATOR: ClassVar[int] = 1 << 18
  F_BOT_HTTP_INTERACTIONS: ClassVar[int] = 1 << 19

  PT_NAME: ClassVar[int] = 0
  PT_NITRO_CLASSIC: ClassVar[int] = 1
  PT_NITRO: ClassVar[int] = 2
  PT_NITRO_BASIC: ClassVar[int] = 3

  id: snowflake
  username: str
  discriminator: str
  global_name: str | None
  avatar: str | None
  bot: bool | Exclude=EXCLUDE
  system: bool | Exclude=EXCLUDE
  mfa_enabled: bool | Exclude=EXCLUDE
  banner: str | None | Exclude=EXCLUDE
  accent_color: int | None | Exclude=EXCLUDE
  locale: str | Exclude=EXCLUDE
  verified: bool | Exclude=EXCLUDE
  email: str | None | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  premium_type: int | Exclude=EXCLUDE
  public_flags: int | Exclude=EXCLUDE
  avatar_decoration_data: AvatarDecorationData | None | Exclude=EXCLUDE
  collectibles: Collectibles | None | Exclude=EXCLUDE
  primary_guild: PrimaryGuild | None | Exclude=EXCLUDE

@dataclass
class GetCurrentUser(__UserBase):
  req_url:  ClassVar[str] = "/@me"
  req_type: ClassVar[str] = "get"

@dataclass
class GetUser(__UserBase):
  req_url:  ClassVar[str] = "/<user.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyCurrentUser(__UserBase):
  req_url:  ClassVar[str] = "/@me"
  req_type: ClassVar[str] = "patch"

  username: str | Exclude=EXCLUDE
  avatar: image_data | None | Exclude=EXCLUDE
  banner: image_data | None | Exclude=EXCLUDE

@dataclass
class GetCurrentUserGuilds(__UserBase):
  req_url:  ClassVar[str] = "/@me/guilds"
  req_type: ClassVar[str] = "get"

@dataclass
class GetCurrentUserGuildMember(__UserBase):
  req_url:  ClassVar[str] = "/@me/guilds/<guild.id>/member"
  req_type: ClassVar[str] = "get"

@dataclass
class LeaveGuild(__UserBase):
  req_url:  ClassVar[str] = "/@me/guilds/<guild.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class CreateDM(__UserBase):
  req_url:  ClassVar[str] = "/@me/channels"
  req_type: ClassVar[str] = "post"

  recipient_id: snowflake

@dataclass
class CreateGroupDM(__UserBase):
  req_url:  ClassVar[str] = "/@me/channels"
  req_type: ClassVar[str] = "post"

  access_tokens: list[str]
  nicks: dict

@dataclass
class GetCurrentUserConnections(__UserBase):
  req_url:  ClassVar[str] = "/@me/connections"
  req_type: ClassVar[str] = "get"

@dataclass
class GetCurrentUserApplicationRoleConnection(__UserBase):
  req_url:  ClassVar[str] = "/@me/applications/<application.id>/role-connection"
  req_type: ClassVar[str] = "get"

@dataclass
class UpdateCurrentUserApplicationRoleConnection(__UserBase):
  req_url:  ClassVar[str] = "/@me/applications/<application.id>/role-connection"
  req_type: ClassVar[str] = "put"

  platform_name: str | Exclude=EXCLUDE
  platform_username: str | Exclude=EXCLUDE
  metadata: b_application_role_connection_metadata.ApplicationRoleConnectionMetadata | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.platform_name, "platform_name", 0, 50)
    format_checker(self.platform_username, "platform_username", 0, 100)
    return super().format_check()

@dataclass
class DeleteCurrentUserApplicationRoleConnection(__UserBase):
  req_url:  ClassVar[str] = "/@me/applications/<application.id>/role-connection"
  req_type: ClassVar[str] = "delete"