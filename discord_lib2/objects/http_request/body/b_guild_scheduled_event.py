from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

snowflake = str
image_data = str
ISO8601timestamp = str

entity_metadata_str = str

@dataclass
class __GuildScheduledEventBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/guilds/<guild.id>/scheduled-event"

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

@dataclass
class N_Weekday:
  n: int
  day: int

@dataclass
class RecurrenceRule:
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
class ListScheduledEventforGuild(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "get"

@dataclass
class CreateGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = ""
  req_type: ClassVar[str] = "post"

  channel_id: snowflake | Exclude
  entity_metadata: entity_metadata_str | Exclude
  name: str
  privacy_level: int
  scheduled_start_time: ISO8601timestamp
  entity_type: int
  recurrence_rule: RecurrenceRule
  scheduled_end_time: ISO8601timestamp | Exclude = Exclude()
  description: str | Exclude = Exclude()
  image: image_data | Exclude = Exclude()

  def format_check(self, filtered_dict):
    not_none_count = 0
    if filtered_dict.get("by_weekday", 0) is not None:
      not_none_count += 1
    if filtered_dict.get("by_n_weekday", 0) is not None:
      not_none_count += 1
    if (filtered_dict.get("by_month", 0) is not None) and (filtered_dict.get("by_month_day", 0) is not None):
      not_none_count += 1
    if not_none_count != 1:
      raise body_base.PayloadFormatError("The values are not mutually exclusive. | name: recurrence_rule")

    if (filtered_dict.get("by_weekday") is not None):
      if filtered_dict.get("frequency") != RRF_DAILY or filtered_dict.get("frequency") != RRF_WEEKLY:
        raise body_base.PayloadFormatError("'by_weekday': The frequency must be DAILY or WEEKLY.")

      if filtered_dict.get("frequency") == RRF_DAILY:
        RRW_check = [RRW_MONDAY_FRIDAY, RRW_TUESDAY_SATURDAY, RRW_SUNDAY_THURSDAY, RRW_FRIDAY_AND_SATURDAY, RRW_SATURDAY_SUNDAY, RRW_SUNDAY_MONDAY]
        if not filtered_dict.get("by_weekday") in RRW_check:
          raise body_base.PayloadFormatError("'by_weekday': This format is not permitted.")
      else:
        if len(filtered_dict.get("by_weekday", "None")) != 1:
          raise body_base.PayloadFormatError("'by_weekday': It must have a length of 1.")

    if filtered_dict.get("by_n_weekday") is not None:
      if filtered_dict.get("frequency") != RRF_MONTHLY:
        raise body_base.PayloadFormatError("'by_n_weekday': The frequency must be MONTHLY.")
      elif len(filtered_dict.get("by_n_weekday", "None")) != 1:
        raise body_base.PayloadFormatError("'by_n_weekday': It must have a length of 1.")
      
    if filtered_dict.get("by_month") is not None:
      if filtered_dict.get("frequency") != RRF_YEARLY:
        raise body_base.PayloadFormatError("'by_month': The frequency must be YEARLY.")
      if (filtered_dict.get("by_month") is None) or (filtered_dict.get("by_month_day") is None):
        raise body_base.PayloadFormatError("'by_month', 'by_month_day': Both of these must be specified.")
      if len(filtered_dict.get("by_month", "None")) != 1:
        raise body_base.PayloadFormatError("'by_month': It must have a length of 1.")
      if len(filtered_dict.get("by_month_day", "None")) != 1:
        raise body_base.PayloadFormatError("'by_month_day': It must have a length of 1.")

    if (filtered_dict.get("interval") != 1) or (filtered_dict.get("interval") != 2):
      raise body_base.PayloadFormatError("'interval': It must be 1 or 2.")
    if filtered_dict.get("interval") == 1:
      pass
    elif filtered_dict.get("interval") == 2:
      if filtered_dict.get("frequency") != RRF_WEEKLY:
        raise body_base.PayloadFormatError("'interval': When the interval is not 1, the frequency must be WEEKLY.")
    else:
      raise body_base.PayloadFormatError("'interval': It must be 1 or 2.")
  
@dataclass
class GetGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class ModifyGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "patch"

  channel_id: snowflake | None | Exclude = Exclude()
  entity_metadata: entity_metadata_str | None | Exclude = Exclude()
  name: str | Exclude = Exclude()
  privacy_level: int | Exclude = Exclude()
  scheduled_start_time: ISO8601timestamp | Exclude = Exclude()
  scheduled_end_time: ISO8601timestamp | Exclude = Exclude()
  description: str | None | Exclude = Exclude()
  entity_type: int | Exclude = Exclude()
  status: int | Exclude = Exclude()
  image: image_data | Exclude = Exclude()
  recurrence_rule: RecurrenceRule | None | Exclude = Exclude()

@dataclass
class DeleteGuildScheduledEvent(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>"
  req_type: ClassVar[str] = "delete"

@dataclass
class GetGuildScheduledEventUsers(__GuildScheduledEventBase):
  req_url:  ClassVar[str] = "/<guild_scheduled_event.id>/users"
  req_type: ClassVar[str] = "get"