from dataclasses import dataclass

from discord_lib2.objects.http_request.request_query.query_base import BaseClass

snowflake = str

@dataclass
class ExecuteWebhook(BaseClass):
  wait: bool
  thread_id: snowflake
  with_components: bool

@dataclass
class ExecuteSlackCompatibleWebhook(BaseClass):
  thread_id: snowflake
  wait: bool

@dataclass
class ExecuteGitHubCompatibleWebhook(BaseClass):
  thread_id: snowflake
  wait: bool

@dataclass
class GetWebhookMessage(BaseClass):
  thread_id: snowflake

@dataclass
class EditWebhookMessage(BaseClass):
  thread_id: snowflake
  with_components: bool

@dataclass
class DeleteWebhookMessage(BaseClass):
  thread_id: snowflake