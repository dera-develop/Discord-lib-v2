from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude
from discord_lib2.objects.http_request.body.body_base import FormFile

from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.http_request.body import b_poll
from discord_lib2.objects.other import component

snowflake = str
image_data = str

@dataclass
class __WebhookBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/webhooks/<webhook.id>"

@dataclass
class CreateWebhook(body_base.BaseClass):
  req_url:  ClassVar[str] = "/channels/<channel.id>/webhooks"
  req_type: ClassVar[str] = "post"

  name: str
  avatar: image_data | None | Exclude = Exclude()

@dataclass
class GetChannelWebhooks(body_base.BaseClass):
  req_url:  ClassVar[str] = "/channels/<channel.id>/webhooks"
  req_type: ClassVar[str] = "get"

@dataclass
class GetGuildWebhooks(body_base.BaseClass):
  req_url:  ClassVar[str] = "/guilds/<guild.id>/webhooks"
  req_type: ClassVar[str] = "get"

@dataclass
class GetWebhook(__WebhookBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class GetWebhookwithToken(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyWebhook(__WebhookBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "patch"

  name: str | Exclude = Exclude()
  avatar: image_data | None | Exclude = Exclude()
  channel_id: snowflake | Exclude = Exclude()

@dataclass
class ModifyWebhookwithToken(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>"
  req_type: ClassVar[str] = "patch"

@dataclass
class DeleteWebhook(__WebhookBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "delete"

@dataclass
class DeleteWebhookwithToken(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>"
  req_type: ClassVar[str] = "delete"

@dataclass
class ExecuteWebhook(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>"
  req_type: ClassVar[str] = "post"

  content: str
  username: str
  avatar_url: str
  tts: bool
  embeds: list[b_message.Embed]
  allowed_mentions: b_message.AllowedMentions
  components: list[component.ComponentClass]
  payload_json: str
  attachments: list[b_message.AttachmentRequest]
  flags: int
  thread_name: str
  applied_tags: list[snowflake]
  poll: b_poll.CreateRequest
  files: FormFile = FormFile()

@dataclass
class ExecuteSlackCompatibleWebhook(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/slack"
  req_type: ClassVar[str] = "post"

@dataclass
class ExecuteGitHubCompatibleWebhook(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/github"
  req_type: ClassVar[str] = "post"

@dataclass
class GetWebhookMessage(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/messages/<message.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class EditWebhookMessage(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/message/<message.id>"
  req_type: ClassVar[str] = "patch"

  content: str | None | Exclude = Exclude()
  embeds: list[b_message.Embed] | None | Exclude = Exclude()
  flags: int | None | Exclude = Exclude()
  allowed_mentions: b_message.AllowedMentions | None | Exclude = Exclude()
  components: list[component.ComponentClass] | None | Exclude = Exclude()
  files: FormFile = FormFile()
  payload_json: str | None | Exclude = Exclude()
  attachments: list[b_message.AttachmentRequest] | None | Exclude = Exclude()
  poll: b_poll.CreateRequest | None | Exclude = Exclude()

@dataclass
class DeleteWebhookMessage(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/messages/<message.id>"
  req_type: ClassVar[str] = "delete"