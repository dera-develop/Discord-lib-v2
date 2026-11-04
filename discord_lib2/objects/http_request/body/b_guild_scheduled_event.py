from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.http_request.format_checker import format_checker, PayloadFormatError

snowflake = str
image_data = str
ISO8601timestamp = str
EXCLUDE = Exclude()

PL_GUILD_ONLY = 2

ET_STAGE_INSTANCE = 1
ET_VOICE = 2
ET_EXTERNAL = 3

RRF_YEARLY = 0
RRF_MONTHLY = 1
RRF_WEEKLY = 2
RRF_DAILY = 3

RRW_MONDAY = 0
RRW_TUESDAY = 1
RRW_WEDNESDAY = 2
RRW_THURSDAY = 3
RRW_FRIDAY = 4
RRW_SATURDAY = 5
RRW_SUNDAY = 6

RRW_MONDAY_FRIDAY = [0, 1, 2, 3, 4]
RRW_TUESDAY_SATURDAY = [1, 2, 3, 4, 5]
RRW_SUNDAY_THURSDAY = [6, 0, 1, 2, 3]
RRW_FRIDAY_AND_SATURDAY = [4, 5]
RRW_SATURDAY_SUNDAY = [5, 6]
RRW_SUNDAY_MONDAY = [6, 0]

RRM_JANUARY = 1
RRM_FEBRUARY = 2
RRM_MARCH = 3
RRM_APRIL = 4
RRM_MAY = 5
RRM_JUNE = 6
RRM_JILY = 7
RRM_AUGUST = 8
RRM_SEPTEMBER = 9
RRM_OCTOVER = 10
RRM_NOVEMBER = 11
RRM_DECEMBER = 12

ES_SCHEDULED = 1
ES_ACTIVE = 2
ES_COMPLETED = 3
ES_CANCELED = 4

# format check
FC_PRIVACY_LEVEL = tuple([PL_GUILD_ONLY])
FC_ENTITY_TYPE = (ET_STAGE_INSTANCE, ET_VOICE, ET_EXTERNAL)

@dataclass
class __GuildScheduledEventBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/scheduled-event"

@dataclass
class N_Weekday(Base):
  n: int
  day: int

@dataclass
class RecurrenceRule(Base):
  start: ISO8601timestamp
  # end: ISO8601timestamp
  frequency: int
  interval: int
  by_weekday: list[int] | None
  by_n_weekday: list[N_Weekday] | None
  by_month: list[int] | None
  by_month_day: list[int] | None
  # by_year_day: list[int] | None
  # count: int | None

@dataclass
class EntityMetadata(Base):
  location: str | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.location, "location", 1, 100)
    return super().format_check()


@dataclass
class ListScheduledEventforGuild(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  name: str
  privacy_level: int
  scheduled_start_time: ISO8601timestamp
  entity_type: int
  recurrence_rule: RecurrenceRule
  channel_id: snowflake | Exclude=EXCLUDE
  entity_metadata: EntityMetadata | Exclude=EXCLUDE
  scheduled_end_time: ISO8601timestamp | Exclude=EXCLUDE
  description: str | Exclude=EXCLUDE
  image: image_data | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.description, "description", 1, 1000)
    format_checker(self.privacy_level, "privacy_level", in_list=FC_PRIVACY_LEVEL)
    format_checker(self.entity_type, "entity_type", in_list=FC_ENTITY_TYPE)
    if isinstance(self.channel_id, Exclude) and self.entity_type != ET_EXTERNAL:
      raise PayloadFormatError("channel_id", "required channel_id if `entity_type` is not `EXTERNAL`")
    if isinstance(self.scheduled_end_time, Exclude) and self.entity_type == ET_EXTERNAL:
      raise PayloadFormatError("scheduled_end_time", "required scheduled_end_time if `entity_type` is `EXTERNAL`")
    return super().format_check()
  
@dataclass
class GetGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "patch"

  channel_id: snowflake | None | Exclude=EXCLUDE
  entity_metadata: EntityMetadata | None | Exclude=EXCLUDE
  name: str | Exclude=EXCLUDE
  privacy_level: int | Exclude=EXCLUDE
  scheduled_start_time: ISO8601timestamp | Exclude=EXCLUDE
  scheduled_end_time: ISO8601timestamp | Exclude=EXCLUDE
  description: str | None | Exclude=EXCLUDE
  entity_type: int | Exclude=EXCLUDE
  status: int | Exclude=EXCLUDE
  image: image_data | Exclude=EXCLUDE
  recurrence_rule: RecurrenceRule | None | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.name, "name", 1, 100)
    format_checker(self.description, "description", 1, 1000)
    format_checker(self.privacy_level, "privacy_level", in_list=FC_PRIVACY_LEVEL)
    format_checker(self.entity_type, "entity_type", in_list=FC_ENTITY_TYPE)
    if self.entity_type == ET_EXTERNAL:
      if self.channel_id is not None:
        raise PayloadFormatError("channel_id", "required and need be set to None if `entity_type` is `EXTERNAL`")
      if not isinstance(self.entity_metadata, EntityMetadata):
        raise PayloadFormatError("entity_metadata", "required entity_metadata if `entity_type` is `EXTERNAL`")
      if not isinstance(self.entity_metadata.location, str):
        raise PayloadFormatError("entity_metadata.location", "required entity_metadata.location if `entity_type` is `EXTERNAL`")
      if not isinstance(self.scheduled_end_time, ISO8601timestamp):
        raise PayloadFormatError("scheduled_end_time", "required scheduled_end_time if `entity_type` is `EXTERNAL`")
    return super().format_check()

@dataclass
class DeleteGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetGuildScheduledEventUsers(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>/users"
  req_type: ClassVar[str] = "get"