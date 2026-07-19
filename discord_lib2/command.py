class FunctionNameDuplicationException(Exception):
  def __init__(self, name: str) -> None:
    super().__init__(name)

class Terminal:
  def __init__(self) -> None:
    self.__command_functions = {}

  def add_command(self, function: function):
    command_name = function.__name__
    if command_name in self.__command_functions:
      raise FunctionNameDuplicationException(command_name)
    self.__command_functions[command_name] = function

  def get_terminal_command(self):
    return self.__command_functions

class Event:
  def __init__(self) -> None:
    pass