from dataclasses import dataclass

from discord_lib2.objects.http_request.query.query_base import BaseClass, Exclude

snowflake = str
EXCLUDE = Exclude()

@dataclass
class ExecuteWebhook(BaseClass):
  wait: bool | Exclude=EXCLUDE
  thread_id: snowflake | Exclude=EXCLUDE
  with_components: bool | Exclude=EXCLUDE

@dataclass
class ExecuteSlackCompatibleWebhook(BaseClass):
  thread_id: snowflake | Exclude=EXCLUDE
  wait: bool | Exclude=EXCLUDE

@dataclass
class ExecuteGitHubCompatibleWebhook(BaseClass):
  thread_id: snowflake | Exclude=EXCLUDE
  wait: bool | Exclude=EXCLUDE

@dataclass
class GetWebhookMessage(BaseClass):
  thread_id: snowflake | Exclude=EXCLUDE

@dataclass
class EditWebhookMessage(BaseClass):
  thread_id: snowflake | Exclude=EXCLUDE
  with_components: bool | Exclude=EXCLUDE

@dataclass
class DeleteWebhookMessage(BaseClass):
  thread_id: snowflake | Exclude=EXCLUDE