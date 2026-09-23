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

#### PRESENCE UPDATE ####
class ActivityTimestamp(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.start: int | None = None
    self.end: int | None = None
  def update(self, data: dict):
    if "start" in data:
      self.start = data.get("start")

    if "end" in data:
      self.end = data.get("end")

class ActivityEmoji(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.name: str | None = None
    self.id: snowflake | None = None
    self.animated: bool | None = None
  def update(self, data: dict):
    if "name" in data:
      self.name = data.get("name")

    if "id" in data:
      self.id = data.get("id")

    if "animated" in data:
      self.animated = data.get("animated")

class ActivityParty(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.id: str | None = None
    self.size: list[int] = []
  def update(self, data: dict):
    if "id" in data:
      self.id = data.get("id")

    if "size" in data:
      size = data.get("size")
      if isinstance(size, list):
        self.size = size

class ActivityAssets(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.large_image: str | None = None
    self.large_text: str | None = None
    self.large_url: str | None = None
    self.small_image: str | None = None
    self.small_text: str | None = None
    self.small_url: str | None = None
    self.invite_cover_image: str | None = None
  def update(self, data: dict):
    if "large_image" in data:
      self.large_image = data.get("large_image")

    if "large_text" in data:
      self.large_text = data.get("large_text")

    if "large_url" in data:
      self.large_url = data.get("large_url")

    if "small_image" in data:
      self.small_image = data.get("small_image")

    if "small_text" in data:
      self.small_text = data.get("small_text")

    if "small_url" in data:
      self.small_url = data.get("small_url")

    if "invite_cover_image" in data:
      self.invite_cover_image = data.get("invite_cover_image")

class ActivitySecrets(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.join: str | None = None
    self.spectate: str | None = None
    self.match: str | None = None
  def update(self, data: dict):
    if "join" in data:
      self.join = data.get("join")

    if "spectate" in data:
      self.spectate = data.get("spectate")

    if "match" in data:
      self.match = data.get("match")

class ActivityButtons(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.label: str | None = None
    self.url: str | None = None
  def update(self, data: dict):
    if "label" in data:
      self.label = data.get("label")

    if "url" in data:
      self.url = data.get("url")

class Activity(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.name: str | None = None
    self.type: int | None = None
    self.url: str | None = None
    self.created_at: int | None = None
    self.timestamps: ActivityTimestamp = ActivityTimestamp()
    self.application_id: snowflake | None = None
    self.status_display_type: int | None = None
    self.details: str | None = None
    self.details_url: str | None = None
    self.state: str | None = None
    self.state_url: str | None = None
    self.emoji: ActivityEmoji = ActivityEmoji()
    self.party: ActivityParty = ActivityParty()
    self.assets: ActivityAssets = ActivityAssets()
    self.secrets: ActivitySecrets = ActivitySecrets()
    self.instance: bool | None = None
    self.flags: int | None = None
    self.buttons: list[ActivityButtons] = []
  def update(self, data: dict):
    if "name" in data:
      self.name = data.get("name")

    if "type" in data:
      self.type = data.get("type")

    if "url" in data:
      self.url = data.get("url")

    if "created_at" in data:
      self.created_at = data.get("created_at")

    if "timestamps" in data:
      timestamps = data.get("timestamps")
      if isinstance(timestamps, dict):
        self.timestamps.update(timestamps)

    if "application_id" in data:
      self.application_id = data.get("application_id")

    if "status_display_type" in data:
      self.status_display_type = data.get("status_display_type")

    if "details" in data:
      self.details = data.get("details")

    if "details_url" in data:
      self.details_url = data.get("details_url")

    if "state" in data:
      self.state = data.get("state")

    if "state_url" in data:
      self.state_url = data.get("state_url")

    if "emoji" in data:
      emoji = data.get("emoji")
      if isinstance(emoji, dict):
        self.emoji.update(emoji)

    if "party" in data:
      party = data.get("party")
      if isinstance(party, dict):
        self.party.update(party)

    if "assets" in data:
      assets = data.get("assets")
      if isinstance(assets, dict):
        self.assets.update(assets)

    if "secrets" in data:
      secrets = data.get("secrets")
      if isinstance(secrets, dict):
        self.secrets.update(secrets)

    if "instance" in data:
      self.instance = data.get("instance")

    if "flags" in data:
      self.flags = data.get("flags")

    if "buttons" in data:
      buttons = data.get("buttons")
      if isinstance(buttons, list):
        bs = []
        for button in buttons:
          button_obj = ActivityButtons()
          button_obj.update(button)
          bs.append(button_obj)
        self.buttons = bs

class ClientStatus(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.desktop: str | None = None
    self.mobile: str | None = None
    self.web: str | None = None
  def update(self, data: dict):
    if "desktop" in data:
      self.desktop = data.get("desktop")

    if "mobile" in data:
      self.mobile = data.get("mobile")

    if "web" in data:
      self.web = data.get("web")

class PresenceUpdate(base.UserCacheBase):
  def __init__(self) -> None:
    super().__init__()
    self.user: snowflake | None = None # user_id
    self.guild_id: snowflake | None = None
    self.status: str | None = None
    self.activities: list[Activity] = []
    self.client_status: ClientStatus = ClientStatus()
  def update(self, data: dict):
    if "user" in data:
      user = data.get("user", {})
      self.user = user.get("id")

    if "guild_id" in data:
      self.guild_id = data.get("guild_id")

    if "status" in data:
      self.status = data.get("status")

    if "activities" in data:
      activities = data.get("activities")
      if isinstance(activities, list):
        acs = []
        for activity in activities:
          activity_obj = Activity()
          activity_obj.update(activity)
          acs.append(activity_obj)
        self.activities = acs

    if "client_status" in data:
      client_status = data.get("client_status")
      if isinstance(client_status, dict):
        self.client_status.update(client_status)
#########################

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
    self.presence: PresenceUpdate = PresenceUpdate()
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