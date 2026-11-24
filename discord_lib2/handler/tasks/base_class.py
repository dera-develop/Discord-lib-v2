import dacite
from logging import Logger
from typing import Callable, Any, TypeVar

from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.handler.cache_update.base_class import HTTPcontroller

T = TypeVar("T")

class TaskBaseClass:
  event_functions: dict[str, Callable] = {}

  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    self.logger = logger
    self.exception_catcher = exception_catcher
    self.data_cache = data_cache
    self.httpapi = http_controller

  def load_object(self, target_class: type[T], source_data: dict[str, Any]) -> T|None:
    try:
      return dacite.from_dict(target_class, source_data)
    except dacite.DaciteError as e:
      self.logger.error(str(e))

  def get_functions(self):
    return self.event_functions