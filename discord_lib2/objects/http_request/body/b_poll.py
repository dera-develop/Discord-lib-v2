from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude, Base

from discord_lib2.objects.http_request.body import b_emoji

from discord_lib2.objects.http_request.format_checker import format_checker

IS08601timestamp = str
EXCLUDE = Exclude()

@dataclass
class __PollBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels/<channel.id>/polls/<message.id>"

@dataclass
class Media(Base):
  text: str | Exclude=EXCLUDE
  emoji: b_emoji.Emoji | Exclude=EXCLUDE

  def format_check(self) -> None:
    format_checker(self.text, "text", 0, 300)
    return super().format_check()

@dataclass
class Answer:
  answer_id: int
  poll_media: Media

@dataclass
class PollResults(Base):
  is_finalized: bool
  answer_counts: list[Answer]

@dataclass
class CreateRequest(Base):
  T_DEFAULT: ClassVar[int] = 1

  question: Media
  answer: list[Answer]
  duration: int | Exclude=EXCLUDE
  allow_multiselect: bool | Exclude=EXCLUDE
  layout_type: int | Exclude=EXCLUDE

@dataclass
class Poll(Base):
  question: Media
  answers: list[Answer]
  expiry: IS08601timestamp | None
  allow_multiselect: bool
  layout_type: int
  results: PollResults | Exclude=EXCLUDE

@dataclass
class GetAnswerVoters(__PollBase):
  req_url:  ClassVar[str] = "/answer/<answer.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class EndPoll(__PollBase):
  req_url:  ClassVar[str] = "/expire"
  req_type: ClassVar[str] = "post"