from dataclasses import dataclass, field
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, FormFile

from discord_lib2.objects.http_request.body import b_message
from discord_lib2.objects.http_request.body import b_poll
from discord_lib2.objects.other import component

from discord_lib2.objects.http_request.format_checker import format_checker

snowflake = str
image_data = str
EXCLUDE = Exclude()

@dataclass
class __WebhookBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/webhooks/<webhook.id>"

@dataclass
class CreateWebhook(body_base.BaseClass):
  req_url:  ClassVar[str] = "/channels/<channel.id>/webhooks"
  req_type: ClassVar[str] = "post"

  name: str
  avatar: image_data | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 80)
    return super().format_check()

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

  name: str | Exclude=EXCLUDE
  avatar: image_data | None | Exclude=EXCLUDE
  channel_id: snowflake | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 80)
    return super().format_check()

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
  files: FormFile = field(default_factory=FormFile)

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    return super().format_check()

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

  content: str | None | Exclude=EXCLUDE
  embeds: list[b_message.Embed] | None | Exclude=EXCLUDE
  flags: int | None | Exclude=EXCLUDE
  allowed_mentions: b_message.AllowedMentions | None | Exclude=EXCLUDE
  components: list[component.ComponentClass] | None | Exclude=EXCLUDE
  files: FormFile = field(default_factory=FormFile)
  payload_json: str | None | Exclude=EXCLUDE
  attachments: list[b_message.AttachmentRequest] | None | Exclude=EXCLUDE
  poll: b_poll.CreateRequest | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.content, "content", 0, 2000)
    return super().format_check()

@dataclass
class DeleteWebhookMessage(__WebhookBase):
  req_url:  ClassVar[str] = "/<webhook.token>/messages/<message.id>"
  req_type: ClassVar[str] = "delete"