from discord_lib2.cache.user import base
from discord_lib2.cache.user import guild

snowflake = base.snowflake
ISO8601timestamp = base.ISO8601timestamp

#### USER PRIMARY GUILD ####
class UserPrimaryGuild(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.identity_guild_id: snowflake | None = None
    self.identity_enabled: bool | None = None
    self.tag: str | None = None
    self.badge: str | None = None
  def update(self, data: dict, delete: bool = False):
    if "identity_guild_id" in data:
      self.identity_guild_id = data.get("identity_guild_id")

    if "identity_enabled" in data:
      self.identity_enabled = data.get("identity_enabled")

    if "tag" in data:
      self.tag = data.get("tag")

    if "badge" in data:
      self.badge = data.get("badge")
############################

#### USER ####
class User(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.id: snowflake | None = None
    self.username: str | None = None
    self.discriminator: str | None = None
    self.global_name: str | None = None
    self.avatar: str | None = None
    self.bot: bool | None = None
    self.system: bool | None = None
    self.mfa_enabled: bool | None = None
    self.banner: str | None = None
    self.accent_color: int | None = None
    self.locale: str | None = None
    self.verified: bool | None = None
    self.email: str | None = None
    self.flags: int | None = None
    self.premium_type: int | None = None
    self.public_flags: int | None = None
    self.avatar_decoration_data: guild.AvatarDecorationData = guild.AvatarDecorationData()
    self.collectibles: guild.Collectibles = guild.Collectibles()
    self.primary_guild: UserPrimaryGuild = UserPrimaryGuild()
    self.joined_guilds: list[snowflake] = []
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "username" in data:
      self.username = data.get("username")

    if "discriminator" in data:
      self.discriminator = data.get("discriminator")

    if "global_name" in data:
      self.global_name = data.get("global_name")

    if "avatar" in data:
      self.avatar = data.get("avatar")

    if "bot" in data:
      self.bot = data.get("bot")

    if "system" in data:
      self.system = data.get("system")

    if "mfa_enabled" in data:
      self.mfa_enabled = data.get("mfa_enabled")

    if "banner" in data:
      self.banner = data.get("banner")

    if "accent_color" in data:
      self.accent_color = data.get("accent_color")

    if "locale" in data:
      self.locale = data.get("locale")

    if "verified" in data:
      self.verified = data.get("verified")

    if "email" in data:
      self.email = data.get("email")

    if "flags" in data:
      self.flags = data.get("flags")

    if "premium_type" in data:
      self.premium_type = data.get("premium_type")

    if "public_flags" in data:
      self.public_flags = data.get("public_flags")

    if "avatar_decoration_data" in data:
      avatar_decoration_data = data.get("avatar_decoration_data")
      if isinstance(avatar_decoration_data, dict):
        self.avatar_decoration_data.update(avatar_decoration_data)

    if "collectibles" in data:
      collectibles = data.get("collectibles")
      if isinstance(collectibles, dict):
        self.collectibles.update(collectibles)

    if "primary_guild" in data:
      primary_guild = data.get("primary_guild")
      if isinstance(primary_guild, dict):
        self.primary_guild.update(primary_guild)
##############