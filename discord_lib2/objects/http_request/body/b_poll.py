from dataclasses import dataclass
from typing import ClassVar

from discord_lib2.objects.http_request.body import body_base
from discord_lib2.objects.http_request.body.body_base import Exclude

from discord_lib2.objects.http_request.body import b_emoji

@dataclass
class __PollBase(body_base.BaseClass):
  req_base_url: ClassVar[str] = "/channels/<channel.id>/polls/<message.id>"

@dataclass
class Media:
  text: str | Exclude = Exclude()
  emoji: b_emoji.Emoji | Exclude = Exclude()

@dataclass
class Answer:
  answer_id: int
  poll_media: Media

@dataclass
class CreateRequest:
  T_DEFAULT: ClassVar[int] = 1

  question: Media
  answer: list[Answer]
  duration: int | Exclude = Exclude()
  allow_multiselect: bool | Exclude = Exclude()
  layout_type: int | Exclude = Exclude()

@dataclass
class GetAnswerVoters(__PollBase):
  req_url:  ClassVar[str] = "/answer/<answer.id>"
  req_type: ClassVar[str] = "get"

@dataclass
class EndPoll(__PollBase):
  req_url:  ClassVar[str] = "/expire"
  req_type: ClassVar[str] = "post"