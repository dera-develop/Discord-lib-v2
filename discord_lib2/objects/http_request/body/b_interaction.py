from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude
from discord_lib2.objects.http_request.body.body_base import FormFile

from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.http_request.body import b_poll
from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.other import component

snowflake = str

@dataclass
class __InteractionBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/webhooks/<application.id>/<interaction.token>"

CALLBACK_PONG = 1
CALLBACK_CHANNEL_MESSAGE_WITH_SOURCE = 4
CALLBACK_DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
CALLBACK_DEFERRED_UPDATE_MESSAGE = 6
CALLBACK_UPDATE_MESSAGE = 7
CALLBACK_APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
CALLBACK_MODAL = 9
CALLBACK_PREMIUM_REQUIRED = 10
CALLBACK_LAUNCH_ACTIVITY = 12

@dataclass
class InteractionCallbackData:
  tts: bool | Exclude = Exclude()
  content: str | Exclude = Exclude()
  embeds: list[b_message.Embed] | Exclude = Exclude()
  allowed_mentions: b_message.AllowedMentions | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  components: list[b_message.component.ComponentClass] | Exclude = Exclude()
  attachments: list[b_message.AttachmentRequest] | Exclude = Exclude()
  poll: b_message.ShardClientTheme | Exclude = Exclude()

@dataclass
class DCChoiceOption:
  name: str
  value: str | int | float

@dataclass
class InteractionCallbackAutocomplete:
  choices: list[DCChoiceOption]

@dataclass
class InteractionCallbackModal:
  custom_id: str
  title: str
  components: list[component.ComponentClass]
  
@dataclass
class CreateInteractionResponse(body_base.BaseClass):
  req_url: ClassVar[str] = "/interactions/<interaction.id>/<interaction.token>/callback"
  req_type: ClassVar[str] = "post"

  type: int
  data: InteractionCallbackData | InteractionCallbackAutocomplete | InteractionCallbackModal | Exclude = Exclude()

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

  content: str | Exclude = Exclude()
  username: str | Exclude = Exclude()
  avatar_url: str | Exclude = Exclude()
  tts: bool | Exclude = Exclude()
  embeds: list[b_message.Embed] | Exclude = Exclude()
  allowed_mentions: b_message.AllowedMentions | Exclude = Exclude()
  components: list[component.ComponentClass] | Exclude = Exclude()
  payload_json: str | Exclude = Exclude()
  attachments: list[b_message.AttachmentRequest] | Exclude = Exclude()
  flags: int | Exclude = Exclude()
  thread_name: str | Exclude = Exclude()
  applied_tags: list[snowflake] | Exclude = Exclude()
  poll: b_poll.CreateRequest | Exclude = Exclude()
  files: FormFile | Exclude = Exclude()

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