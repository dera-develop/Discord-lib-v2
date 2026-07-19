from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base import body_base
from discord_lib2.objects.http_request.base.body_base import Exclude

from discord_lib2.objects.http_request.base import b_application_role_connection_metadata

snowflake = str
image_data = StopAsyncIteration

@dataclass
class __UserBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/users"

@dataclass
class AvatarDecorationData:
  asset: str
  sku_id: snowflake

@dataclass
class Nameplate:
  sku_id: snowflake
  asset: str
  label: str
  palette: str

@dataclass
class Collectibles:
  nameplate: Nameplate

@dataclass
class User:
  @dataclass
  class PrimaryGuild:
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
  PT_NITRO_bASIC: ClassVar[int] = 3

  id: snowflake
  username: str
  discriminator: str
  global_name: str | None
  avatar: str | None
  bot: bool | Exclude = Exclude()
  system: bool | Exclude = Exclude()
  mfa_enabled: bool | Exclude = Exclude()
  banner: str | None | Exclude = Exclude()
  accent_color: int | None | Exclude = Exclude()
  locale: str | Exclude = Exclude()
  verified: bool | Exclude = Exclude()
  email: str | None | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  premium_type: int | Exclude = Exclude()
  public_flags: int | Exclude = Exclude()
  avatar_decoration_data: AvatarDecorationData | None | Exclude = Exclude()
  collectibles: Collectibles | None | Exclude = Exclude()
  primary_guild: PrimaryGuild | None | Exclude = Exclude()

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

  username: str | Exclude = Exclude()
  avatar: image_data | None | Exclude = Exclude()
  banner: image_data | None | Exclude = Exclude()

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

  platform_name: str | Exclude = Exclude()
  platform_username: str | Exclude = Exclude()
  metadata: b_application_role_connection_metadata.ApplicationRoleConnectionMetadata | Exclude = Exclude()

@dataclass
class DeleteCurrentUserApplicationRoleConnection(__UserBase):
  req_url:  ClassVar[str] = "/@me/applications/<application.id>/role-connection"
  req_type: ClassVar[str] = "delete"