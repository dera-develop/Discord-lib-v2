from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, FormFile, Base

from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.http_request.body import b_poll
from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.other import component

from discord_lib2.objects.http_request.format_checker import format_checker, PayloadFormatError
from discord_lib2.objects import locales

snowflake = str
EXCLUDE = Exclude()

@dataclass
class __InteractionBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/webhooks/<application.id>/<interaction.token>"

CT_PONG = 1
CT_CHANNEL_MESSAGE_WITH_SOURCE = 4
CT_DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
CT_DEFERRED_UPDATE_MESSAGE = 6
CT_UPDATE_MESSAGE = 7
CT_APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
CT_MODAL = 9
CT_PREMIUM_REQUIRED = 10
CT_LAUNCH_ACTIVITY = 12

FC_INTERACTION_CALLBACK_TYPE = (
  CT_PONG, CT_CHANNEL_MESSAGE_WITH_SOURCE, CT_DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE, CT_DEFERRED_UPDATE_MESSAGE, CT_UPDATE_MESSAGE,
  CT_APPLICATION_COMMAND_AUTOCOMPLETE_RESULT, CT_MODAL, CT_PREMIUM_REQUIRED, CT_LAUNCH_ACTIVITY
)

@dataclass
class InteractionCallbackMessage(Base):
  tts: bool | Exclude=EXCLUDE
  content: str | Exclude=EXCLUDE
  embeds: list[b_message.Embed] | Exclude=EXCLUDE
  allowed_mentions: b_message.AllowedMentions | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  components: list[b_message.component.ComponentClass] | Exclude=EXCLUDE
  attachments: list[b_message.AttachmentRequest] | Exclude=EXCLUDE
  poll: b_message.ShardClientTheme | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    format_checker(self.embeds, "embeds", 0, 10)
    return super().format_check()

@dataclass
class ACChoiceOption(Base):
  name: str
  value: str | int | float
  name_localizations: dict[str, str] | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    if isinstance(self.value, str):
      format_checker(self.value, "value", 0, 100)
    if isinstance(self.name_localizations, dict):
      for k, v in self.name_localizations.items():
        if k not in locales.LOCALES.keys():
          PayloadFormatError("name_localizations", f"unknown locale: {k}")
        format_checker(v, f"name_localizations.{k}", 1, 100)
    return super().format_check()

@dataclass
class InteractionCallbackAutocomplete(Base):
  choices: list[ACChoiceOption]

  def format_check(self) -> None:
    format_checker(self.choices, "choices", 0, 25)
    return super().format_check()

@dataclass
class InteractionCallbackModal(Base):
  custom_id: str
  title: str
  components: list[component.ComponentClass]

  def format_check(self) -> None:
    format_checker(self.custom_id, "custom_id", 1, 100)
    format_checker(self.title, "title", 0, 45)
    format_checker(self.components, "components", 1, 5)
    return super().format_check()
  
@dataclass
class CreateInteractionResponse(body_base.BaseClass):
  req_url: ClassVar[str] = "/interactions/<interaction.id>/<interaction.token>/callback"
  req_type: ClassVar[str] = "post"

  type: int
  data: InteractionCallbackMessage | InteractionCallbackAutocomplete | InteractionCallbackModal | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.type, "type", in_list=FC_INTERACTION_CALLBACK_TYPE)
    return super().format_check()

@dataclass
class GetOriginalInteractionResponse(__InteractionBase):
  req_url: ClassVar[str] = "/messages/@original"
  req_type: ClassVar[str] = "get"

@dataclass
class EditOriginalInteractionResponse(__InteractionBase):
  req_url: ClassVar[str] = "/messages/@original"
  req_type: ClassVar[str] = "patch"

@dataclass
class DeleteOriginalInteractionResponse(__InteractionBase):
  req_url: ClassVar[str] = "/messages/@original"
  req_type: ClassVar[str] = "delete"

@dataclass
class CreateFollowupMessage(__InteractionBase):
  req_url: ClassVar[str] = ""
  req_type = "post"

  content: str | Exclude=EXCLUDE
  username: str | Exclude=EXCLUDE
  avatar_url: str | Exclude=EXCLUDE
  tts: bool | Exclude=EXCLUDE
  embeds: list[b_message.Embed] | Exclude=EXCLUDE
  allowed_mentions: b_message.AllowedMentions | Exclude=EXCLUDE
  components: list[component.ComponentClass] | Exclude=EXCLUDE
  payload_json: str | Exclude=EXCLUDE
  attachments: list[b_message.AttachmentRequest] | Exclude=EXCLUDE
  flags: int | Exclude=EXCLUDE
  thread_name: str | Exclude=EXCLUDE
  applied_tags: list[snowflake] | Exclude=EXCLUDE
  poll: b_poll.CreateRequest | Exclude=EXCLUDE
  files: FormFile | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    format_checker(self.embeds, "embeds", 0, 10)
    return super().format_check()

@dataclass
class GetFollowupMessage(__InteractionBase):
  req_url = "/messages/<message.id>"
  req_type = "get"

@dataclass
class EditFollowupMessage(__InteractionBase):
  req_url = "/messages/<message.id>"
  req_type = "patch"

@dataclass
class DeleteFollowupMessage(__InteractionBase):
  req_url = "/messages/<message.id>"
  req_type = "delete"