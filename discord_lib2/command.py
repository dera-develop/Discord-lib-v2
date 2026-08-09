from discord_lib2.objects.resources import UserTerminalCommandResources
from typing import Callable, Awaitable

class TerminalCommand:
  class AlreadyDeclaredException(Exception):
    def __init__(self, *args: object) -> None:
      super().__init__(*args)

  def __init__(self) -> None:
    self.user_command_functions: dict[str, Callable[[list[str], UserTerminalCommandResources], Awaitable[None]]] = {}

  def add_command(self, command_name: str, function: Callable[[list[str], UserTerminalCommandResources], Awaitable[None]]):
    if command_name in self.user_command_functions:
      raise self.AlreadyDeclaredException(command_name)
    self.user_command_functions[command_name] = function