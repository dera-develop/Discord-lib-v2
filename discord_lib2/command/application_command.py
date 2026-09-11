from discord_lib2.objects import locales
from discord_lib2.objects import resources
from discord_lib2.objects.gateway.recv_event_object import Interaction

from discord_lib2.objects.http_request.body import b_interaction
from discord_lib2.objects.http_request.body.b_interaction import InteractionCallbackData
from discord_lib2.command.appcom_get_exe_data import AppComArgs

##########################################################################################
class AlreadyExistsError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class FormatError(Exception):
  LENGTH = "length_error"
  VALUE_RANGE = "value_range_error"
  INVALID_TYPE = "invalid_type_error"
  OTHER = "other_error"
  def __init__(self, value_name: str, reason: str, description: str="") -> None:
    super().__init__(f"Format error | value: {value_name}, reason: {reason} | {description}")

##########################################################################################
class __CommandBase:
  _type: int = -1
  name: str = ""
  description: str = ""
  name_localizations: dict[str, str] | None = None
  description_localizations: dict[str, str] | None = None

  def add_name_localization(self, locale: str, name: str):
    if self.name_localizations is None:
      self.name_localizations = {}
    if not locale in locales.LOCALES:
      raise KeyError(locale)
    if locale in self.name_localizations:
      raise AlreadyExistsError(locale)
    self.name_localizations[locale] = name

  def add_description_localization(self, locale: str, description: str):
    if self.description_localizations is None:
      self.description_localizations = {}
    if not locale in locales.LOCALES:
      raise KeyError(locale)
    if locale in self.description_localizations:
      raise AlreadyExistsError(locale)
    self.description_localizations[locale] = description

  def _format_check(self):
    if not 1 <= len(self.name) <= 32:
      raise FormatError("name", FormatError.LENGTH, f"size: 1~32, now: {len(self.name)}")
    if not 1 <= len(self.description) <= 100:
      raise FormatError("description", FormatError.LENGTH, f"size: 1~100, now: {len(self.description)}")
    if self.name_localizations is not None:
      for l, n in self.name_localizations.items():
        if not 1 <= len(n) <= 32:
          raise FormatError(f"name_{l}", FormatError.LENGTH, f"size: 1~32, now: {len(n)}")
    if self.description_localizations is not None:
      for l, d in self.description_localizations.items():
        if not 1 <= len(d) <= 100:
          raise FormatError(f"description_{l}", FormatError.LENGTH, f"size: 1~100, now: {len(d)}")

  def _get(self):
    self._format_check()
    return_dict = {
      "type": self._type,
      "name": self.name,
      "description": self.description
    }
    if self.name_localizations is not None:
      return_dict["name_localizations"] = self.name_localizations
    if self.description_localizations is not None:
      return_dict["description_localizations"] = self.description_localizations
    return return_dict

##########################################################################################
class ChoiceOption:
  def __init__(self, name: str, value: str | int | float) -> None:
    self.__dict = {
      "name": name,
      "name_localizations": None,
      "value": value
    }

  def add_localization(self, locale: str, name: str):
    if not locale in locales.LOCALES:
      KeyError(locale)
    if self.__dict["name_localizations"] is None:
      self.__dict["name_localizations"] = {}
    self.__dict["name_localizations"][locale] = name

  def _format_check(self):
    if not 1 <= len(self.__dict["name"]) <= 100:
      raise FormatError("name", FormatError.LENGTH, f"size: 1~100, now: {len(self.__dict["name"])}")
    if isinstance(self.__dict["value"], str):
      if not 1 <= len(self.__dict["value"]) <= 100:
        raise FormatError("value", FormatError.LENGTH, f"size: 1~100, now: {len(self.__dict["value"])}")
    if self.__dict["name_localizations"] is not None:
      for l, n in self.__dict["name_localizations"].items():
        if not 1 <= len(n) <= 100:
          raise FormatError(f"name_{l}", FormatError.LENGTH, f"size: 1~100, now: {len(n)}")

  def _get(self):
    return self.__dict

##########################################################################################
class _OptionsBase(__CommandBase):
  required: bool=False
  def _get(self):
    return_dict = super()._get()
    return_dict["required"] = self.required
    return return_dict

class String(_OptionsBase):
  _type = 3
  choices: list[ChoiceOption] | None=None
  min_length: int | None=None
  max_length: int | None=None
  autocomplete: bool | None=None
  def _format_check(self):
    if self.choices is not None:
      if not len(self.choices) > 25:
        FormatError("choices", FormatError.LENGTH, f"max: 25, now: {len(self.choices)}")
    if self.min_length is not None:
      if not 0 <= self.min_length <= 6000:
        FormatError("min_length", FormatError.VALUE_RANGE, f"range: 0~6000, now: {self.min_length}")
    if self.max_length is not None:
      if not 0 <= self.max_length <= 6000:
        FormatError("max_length", FormatError.VALUE_RANGE, f"range: 0~6000, now: {self.max_length}")
    return super()._format_check()

  def _get(self):
    return_dict = super()._get()
    if self.choices is not None:
      return_dict["choices"] = [choice._get() for choice in self.choices]
    if self.min_length is not None:
      return_dict["min_length"] = self.min_length
    if self.max_length is not None:
      return_dict["max_length"] = self.max_length
    if self.autocomplete is not None:
      return_dict["autocomplete"] = self.autocomplete
    return return_dict

class Integer(_OptionsBase):
  _type = 4
  choices: list[ChoiceOption] | None=None
  min_value: int | None=None
  max_value: int | None=None
  autocomplete: bool | None=None
  def _format_check(self):
    if self.choices is not None:
      if not len(self.choices) > 25:
        FormatError("choices", FormatError.LENGTH, f"max: 25, now: {len(self.choices)}")
    return super()._format_check()

  def _get(self):
    return_dict = super()._get()
    if self.choices is not None:
      return_dict["choices"] = [choice._get() for choice in self.choices]
    if self.min_value is not None:
      return_dict["min_value"] = self.min_value
    if self.max_value is not None:
      return_dict["max_value"] = self.max_value
    if self.autocomplete is not None:
      return_dict["autocomplete"] = self.autocomplete
    return return_dict

class Boolean(_OptionsBase):
  _type = 5

class User(_OptionsBase):
  _type = 6

class Channel(_OptionsBase):
  _type = 7
  channel_types: list[int] | None=None
  def _format_check(self):
    if self.channel_types is not None:
      for ct in self.channel_types:
        if not 0 <= ct <= 16:
          raise FormatError("channel_types", FormatError.INVALID_TYPE, f"channel_type(0~16), now: {ct}")
    return super()._format_check()

  def _get(self):
    return_dict = super()._get()
    if self.channel_types is not None:
      return_dict["channel_types"] = list(set(self.channel_types))
    return return_dict

class Role(_OptionsBase):
  _type = 8

class Mentionable(_OptionsBase):
  _type = 9

class Number(_OptionsBase):
  _type = 10
  choices: list[ChoiceOption] | None=None
  min_value: float | None=None
  max_value: float | None=None
  autocomplete: bool | None=None
  def _format_check(self):
    if self.choices is not None:
      if not len(self.choices) > 25:
        FormatError("choices", FormatError.LENGTH, f"max: 25, now: {len(self.choices)}")
    return super()._format_check()

  def _get(self):
    return_dict = super()._get()
    if self.choices is not None:
      return_dict["choices"] = [choice._get() for choice in self.choices]
    if self.min_value is not None:
      return_dict["min_value"] = self.min_value
    if self.max_value is not None:
      return_dict["max_value"] = self.max_value
    if self.autocomplete is not None:
      return_dict["autocomplete"] = self.autocomplete
    return return_dict

class Attachment(_OptionsBase):
  _type = 11
  file_types: list[str] | None=None
  def _format_check(self):
    if self.file_types is not None:
      if len(self.file_types) > 10:
        FormatError("file_types", FormatError.VALUE_RANGE, f"max: 10, now: {len(self.file_types)}")
      for ft in self.file_types:
        if len(ft) < 2:
          FormatError("file_types", FormatError.INVALID_TYPE, f"error_type: {ft}")
        if ft[0] != ".":
          FormatError("file_types", FormatError.INVALID_TYPE, f"need\".\", error_type: {ft}")
    return super()._format_check()

  def _get(self):
    return_dict = super()._get()
    if self.file_types is not None:
      return_dict["file_types"] = self.file_types
    return return_dict

##########################################################################################
class SubCommand(__CommandBase):
  _type = 1
  options: list[dict] | None=None
  interaction_type: int = 4
  interaction_callback_message: b_interaction.InteractionCallbackData | None=None
  def add_option(self, command_option: _OptionsBase):
    if self.options is None:
      self.options = []
    self.options.append(command_option._get())

  def _get(self):
    return_dict = super()._get()
    if self.options is not None:
      return_dict["options"] = self.options
    return return_dict

  def command_function(self, interaction: Interaction, resources: resources.ApplicationCommandResources, args: AppComArgs):
    pass

##########################################################################################
class SubCommandGroup(__CommandBase):
  _type = 2
  options: list[dict] | None=None
  def __init__(self) -> None:
    super().__init__()
    self.__response_datas: dict = {}

  def add_subcommand(self, subcommand: SubCommand):
    if self.options is None:
      self.options = []
    self.options.append(subcommand._get())
    self.__response_datas[subcommand.name] = {
      "__func": subcommand.command_function,
      "__imsg": subcommand.interaction_callback_message,
      "__itype": subcommand.interaction_type
    }

  def _get(self):
    return_dict = super()._get()
    if self.options is not None:
      return_dict["options"] = self.options
    return return_dict

  def _get_functions(self):
    return self.__response_datas

##########################################################################################
class GuildApplicationCommand(__CommandBase):
  _type = 1
  type: int = 1
  default_member_permissions: str | None=None
  default_permission: bool | None=None
  nsfw: bool = False
  options: list[dict] | None=None
  interaction_type: int = 4
  interaction_callback_message: b_interaction.InteractionCallbackData | None=None
  def __init__(self) -> None:
    super().__init__()
    self.__response_datas: dict = {}

  def add_option(self, options: SubCommandGroup | SubCommand | _OptionsBase):
    if self.options is None:
      self.options = []
    self.options.append(options._get())
    if isinstance(options, SubCommandGroup):
      self.__response_datas[options.name] = options._get_functions()
    elif isinstance(options, SubCommand):
      self.__response_datas[options.name] = {
        "__func": options.command_function,
        "__imsg": options.interaction_callback_message,
        "__itype": options.interaction_type
      }

  def _get(self):
    return_dict = super()._get()
    return_dict["nsfw"] = self.nsfw
    return_dict["type"] = self.type
    if self.default_member_permissions is not None:
      return_dict["default_member_permissions"] = self.default_member_permissions
    if self.default_permission is not None:
      return_dict["default_permission"] = self.default_permission
    if self.options is not None:
      return_dict["options"] = self.options
    return return_dict

  def _get_functions(self):
    self.__response_datas["__func"] = self.command_function
    self.__response_datas["__imsg"] = self.interaction_callback_message
    self.__response_datas["__itype"] = self.interaction_type
    return self.__response_datas

  def command_function(self, interaction: Interaction, resources: resources.ApplicationCommandResources, args: AppComArgs):
    pass

##########################################################################################
class GlobalApplicationCommand(__CommandBase):
  _type = 1
  type: int = 1
  default_member_permissions: str | None=None
  default_permission: bool | None=None
  nsfw: bool = False
  global_integration_types: list[int] | None=None
  global_contexts: list[int] | None=None
  global_handler: int | None=None
  interaction_type: int = 4
  interaction_callback_message: b_interaction.InteractionCallbackData | None=None
  def __init__(self) -> None:
    super().__init__()
    self.__response_datas: dict = {}

  def add_option(self, options: SubCommandGroup | SubCommand | _OptionsBase):
    if self.options is None:
      self.options = []
    self.options.append(options._get())
    if isinstance(options, SubCommand):
      self.__response_datas[options.name] = {
        "__func": options.command_function,
        "__imsg": options.interaction_callback_message,
        "__itype": options.interaction_type
      }
    elif isinstance(options, SubCommandGroup):
      self.__response_datas[options.name] = options._get_functions()

  def _get(self):
    return_dict = super()._get()
    return_dict["nsfw"] = self.nsfw
    return_dict["type"] = self.type
    if self.default_member_permissions is not None:
      return_dict["default_member_permissions"] = self.default_member_permissions
    if self.default_permission is not None:
      return_dict["default_permission"] = self.default_permission
    if self.global_integration_types is not None:
      return_dict["integration_types"] = self.global_integration_types
    if self.global_contexts is not None:
      return_dict["contexts"] = self.global_contexts
    if self.global_handler is not None:
      return_dict["handler"] = self.global_handler
    if self.options is not None:
      return_dict["options"] = self.options
    return return_dict

  def _get_functions(self):
    self.__response_datas["__func"] = self.command_function
    self.__response_datas["__imsg"] = self.interaction_callback_message
    self.__response_datas["__itype"] = self.interaction_type
    return self.__response_datas

  def command_function(self, interaction: Interaction, resources: resources.ApplicationCommandResources, args: AppComArgs):
    pass