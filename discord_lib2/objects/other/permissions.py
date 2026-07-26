from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.base.body_base import Exclude

snowflake = str

@dataclass
class Role:
  @dataclass
  class Colors:
    primary_color: int
    secondary_color: int | None
    tertiary_color: int | None

  @dataclass
  class Tags:
    bot_id: snowflake | Exclude = Exclude()
    integration_id: snowflake | Exclude = Exclude()
    premium_subscriber: None | Exclude = Exclude()
    subscription_listing_id: snowflake | Exclude = Exclude()
    available_for_purchase: None | Exclude = Exclude()
    guild_connection: None | Exclude = Exclude()

  F_IN_PROMPT: ClassVar[int] = 1 << 0

  id: snowflake
  name: str
  color: int
  colors: Colors
  hoist: bool
  position: int
  permissions: str
  managed: bool
  mentionable: bool
  tags: Tags
  flags: int
  icom: str | None | Exclude = Exclude()
  unicode_emoji: str | None | Exclude = Exclude()