from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body.body_base import Exclude
from discord_lib2.objects.http_request.body import b_emoji

snowflake = str

@dataclass
class ComponentClass:
  pass

@dataclass
class UnfurledMediaItem:
  IF_IS_ANIMATED: ClassVar[int] = 1 << 0

  url: str
  proxy_url: str | Exclude = Exclude()
  height: int | None | Exclude = Exclude()
  width: int | None | Exclude = Exclude()
  placeholder: str | Exclude = Exclude()
  placeholder_version: int | Exclude = Exclude()
  content_type: str | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  attachment_id: snowflake | Exclude = Exclude()

@dataclass
class ActionRow(ComponentClass):
  components: list[ComponentClass]
  type: int = 1
  id: int | Exclude = Exclude()

@dataclass
class Button(ComponentClass):
  S_PRIMARY: ClassVar[int] = 1
  S_SECONDARY: ClassVar[int] = 2
  S_SUCCESS: ClassVar[int] = 3
  S_DANGER: ClassVar[int] = 4
  S_LINK: ClassVar[int] = 5
  S_PREMIUM: ClassVar[int] = 6

  style: int
  label: str | Exclude = Exclude()
  emoji: b_emoji.Emoji | Exclude = Exclude()
  custom_id: str | Exclude = Exclude()
  sku_id: snowflake | Exclude = Exclude()
  url: str | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 2
  id: int | Exclude = Exclude()

@dataclass
class StringSelect(ComponentClass):
  @dataclass
  class SelectOption:
    label: str
    value: str
    description: str | Exclude = Exclude()
    emoji: b_emoji.Emoji | Exclude = Exclude()
    default: bool | Exclude = Exclude()

  custom_id: str
  options: list[SelectOption]
  placeholder: str | Exclude = Exclude()
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 3
  id: int | Exclude = Exclude()

@dataclass
class TextInput(ComponentClass):
  S_SHORT: ClassVar[int] = 1
  S_PARAGRAPH: ClassVar[int] = 2

  custom_id: str
  style: int
  min_length: int | Exclude = Exclude()
  max_length: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  value: str | Exclude = Exclude()
  placeholder: str | Exclude = Exclude()

  type: int = 4
  id: int | Exclude = Exclude()

@dataclass
class UserSelect(ComponentClass):
  @dataclass
  class SelectDefaultValue:
    id: snowflake
    type: str

  custom_id: str
  placeholder: str | Exclude = Exclude()
  default_values: list[SelectDefaultValue] | Exclude = Exclude()
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 5
  id: int | Exclude = Exclude()

@dataclass
class RoleSelect(ComponentClass):
  @dataclass
  class SelectDefaultValue:
    id: snowflake
    type: str

  custom_id: str
  placeholder: str | Exclude = Exclude()
  default_values: list[SelectDefaultValue] | Exclude = Exclude()
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 6
  id: int | Exclude = Exclude()

@dataclass
class MentionableSelect(ComponentClass):
  @dataclass
  class SelectDefaultValue:
    id: snowflake
    type: str

  custom_id: str
  placeholder: str | Exclude = Exclude()
  default_values: list[SelectDefaultValue] | Exclude = Exclude()
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 7
  id: int | Exclude = Exclude()

@dataclass
class ChannelSelect(ComponentClass):
  @dataclass
  class SelectDefaultValue:
    id: snowflake
    type: str

  custom_id: str
  channel_types: list[int] | Exclude = Exclude()
  placeholder: str | Exclude = Exclude()
  default_values: list[SelectDefaultValue] | Exclude = Exclude()
  min_value: int | Exclude = Exclude()
  max_value: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()
  disabled: bool | Exclude = Exclude()

  type: int = 8
  id: int | Exclude = Exclude()

@dataclass
class Section(ComponentClass):
  components: list[ComponentClass]
  accessory: ComponentClass

  type: int = 9
  id: int | Exclude = Exclude()

@dataclass
class TextDisplay(ComponentClass):
  content: str

  type: int = 10
  id: int | Exclude = Exclude()

@dataclass
class Thumbnail(ComponentClass):
  media: UnfurledMediaItem
  description: str | None | Exclude = Exclude()
  spoiler: bool | Exclude = Exclude()

  type: int = 11
  id: int | Exclude = Exclude()

@dataclass
class MediaGallery(ComponentClass):
  @dataclass
  class Item:
    media: UnfurledMediaItem
    description: str | None | Exclude = Exclude()
    spoiler: bool | Exclude = Exclude()

  items: list[Item]

  type: int = 12
  id: int | Exclude = Exclude()

@dataclass
class File(ComponentClass):
  file: UnfurledMediaItem
  spoiler: bool | Exclude = Exclude()
  name: str | Exclude = Exclude()
  size: int | Exclude = Exclude()

  type: int = 13
  id: int | Exclude = Exclude()

@dataclass
class Separator(ComponentClass):
  divider: bool | Exclude = Exclude()
  spacing: int | Exclude = Exclude()

  type: int = 14
  id: int | Exclude = Exclude()

@dataclass
class Container(ComponentClass):
  components: list[ComponentClass]
  accent_color: int | None | Exclude = Exclude()
  spoiler: bool | Exclude = Exclude()

  type: int = 17
  id: int | Exclude = Exclude()

@dataclass
class Label(ComponentClass):
  label: str
  component: ComponentClass
  description: str | Exclude = Exclude()
  type: int = 18
  id: int | Exclude = Exclude()

@dataclass
class FileUpload(ComponentClass):
  custom_id: str
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()

  type: int = 19
  id: int | Exclude = Exclude()

@dataclass
class RadioGroup(ComponentClass):
  @dataclass
  class Option:
    value: str
    label: str
    description: str | Exclude = Exclude()
    default: bool | Exclude = Exclude()

  custom_id: str
  options: list[Option]
  required: bool | Exclude = Exclude()

  type: int = 21
  id: int | Exclude = Exclude()

@dataclass
class CheckboxGroup(ComponentClass):
  @dataclass
  class Option:
    value: str
    label: str
    description: str
    default: bool

  custom_id: str
  options: list[Option]
  min_values: int | Exclude = Exclude()
  max_values: int | Exclude = Exclude()
  required: bool | Exclude = Exclude()

  type: int = 22
  id: int | Exclude = Exclude()

@dataclass
class Checkbox(ComponentClass):
  custom_id: str
  default: bool | Exclude = Exclude()
  type: int = 23
  id: int | Exclude = Exclude()