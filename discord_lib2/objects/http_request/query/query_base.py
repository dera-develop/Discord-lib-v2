from dataclasses import dataclass, fields

class Exclude:
  pass

@dataclass
class Base:
  def format_check(self) -> None:
    pass

@dataclass
class BaseClass(Base):
  def __asdict_q_exclude_filter(self) -> dict:
    return_dict = {}
    for key, value in self.__dict__.items():
      if not isinstance(value, Exclude):
        return_dict[key] = str(value)
    return return_dict

  def get(self) -> dict:
    self.format_check()
    class_dict = self.__asdict_q_exclude_filter()
    return class_dict