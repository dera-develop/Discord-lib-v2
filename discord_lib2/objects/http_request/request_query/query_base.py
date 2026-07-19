class Exclude:
  pass

class BaseClass:
  def __asdict_q_exclude_filter(self) -> dict:
    return_dict = {}
    for key, value in self.__dict__.items():
      if not isinstance(value, Exclude):
        return_dict[key] = str(value)
    return return_dict
  
  def format_check(self, filtered_dict) -> None:
    pass

  def get(self) -> dict:
    class_dict = self.__asdict_q_exclude_filter()
    self.format_check(class_dict)
    return class_dict