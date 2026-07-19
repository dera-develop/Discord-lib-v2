import asyncio

from discord_lib2.logger import Logger

class Terminal:
  input_queue: asyncio.Queue
  def __init__(self, logger: Logger) -> None:
    self.input_queue = asyncio.Queue()
    self.logger = logger.get_child("TLN")

  async def __worker_terminal_listener(self):
    self.logger.info("Task started | name: worker=terminal_listener")
    try:
      while True:
        inputted_command = await asyncio.to_thread(input, "")
        inputted_command = inputted_command.strip()
        self.logger.info(f"input | {inputted_command}")
        await self.input_queue.put(inputted_command)
        await asyncio.sleep(0.1)
    
    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"worker error | reason: {str(e)}")

  async def start(self):
    self.__task__terminal_listener = asyncio.create_task(self.__worker_terminal_listener())

  async def stop(self):
    if self.__task__terminal_listener:
      self.__task__terminal_listener.cancel()
      try:
        await self.__task__terminal_listener
      except:
        pass
      finally:
        self.logger.info("Task stopped | name: worker=terminal_listener")

  async def get_input(self):
    inputted_command = self.input_queue.get_nowait()
    self.input_queue.task_done()
    return inputted_command