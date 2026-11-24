from logging import Logger
from typing import Any
from itertools import chain

from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.handler.cache_update.base_class import HTTPcontroller
from discord_lib2.handler.tasks.base_class import TaskBaseClass
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.objects.resources import ApplicationCommandResources

from discord_lib2.command.appcom_updator import update_appcom
from discord_lib2.command.appcom_get_exe_data import get_appcom_exedata, get_autocomplete_func
from discord_lib2.command.application_command import GlobalApplicationCommand, GuildApplicationCommand
from discord_lib2.objects.gateway import recv_event_object

from discord_lib2.objects.http_request.body import b_interaction

class TaskApplicationCommand(TaskBaseClass):
  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller, system_cache: SystemCacheVault, appcom_resources: ApplicationCommandResources, guild_appcoms: dict[str, dict[str, GuildApplicationCommand]], global_appcoms: dict[str, GlobalApplicationCommand]) -> None:
    super().__init__(logger, exception_catcher, data_cache, http_controller)
    self.system_cache = system_cache
    self.appcom_resources = appcom_resources
    self.guild_appcoms = guild_appcoms
    self.global_appcoms = global_appcoms
    self.event_functions = {
      "GUILD_CREATE": self.update_guild_appcom,
      "INTERACTION_CREATE": self.interaction
    }

  def __get_global_appcom(self, name: str) -> GlobalApplicationCommand|None:
    global_appcom = self.global_appcoms.get(name)
    if global_appcom is None:
      self.logger.error(f"command \"{name}\" is not registered to global application command")
      return
    return global_appcom

  def __get_guild_appcom(self, name: str, guild_id: str) -> GuildApplicationCommand|None:
    guild_appcom = self.guild_appcoms.get(guild_id)
    if guild_appcom is None:
      guild_appcom = self.guild_appcoms.get("any")
    if guild_appcom is None:
      self.logger.error(f"cache error | guild not registered | id: {guild_id}")
      return
    guild_appcom = guild_appcom.get(name)
    if guild_appcom is None:
      self.logger.error(f"command \"{name}\" is not registered to guild {guild_id}.")
      return
    return guild_appcom

  async def update_guild_appcom(self, event_data: dict[str, Any]):
    if event_data.get("unavailable"): return
    guild_id: str = event_data["id"]
    get_guild_appcoms = list(self.guild_appcoms.get(guild_id, {}).values())
    get_any_appcoms = list(self.guild_appcoms.get("any", {}).values())
    new_appcoms_data = list(chain(get_guild_appcoms, get_any_appcoms))
    await update_appcom(self.logger, self.httpapi.loader, self.httpapi.request, self.data_cache.data.application.id, new_appcoms_data, guild_id)

  ### ping execution ###
  async def __interaction_exe_ping(self):
    pass
  ######################

  ### application command execution ###
  async def __execution_global_application_command(self, interaction_obj: recv_event_object.ApplicationCommandInteraction):
    global_appcom = self.__get_global_appcom(interaction_obj.data.name)
    if global_appcom is None: return
    exe_infos = get_appcom_exedata(interaction_obj.data.options, global_appcom._get_functions())
    await exe_infos.func(interaction_obj, self.appcom_resources, exe_infos.args)

  async def __execution_guild_application_command(self, interaction_obj: recv_event_object.ApplicationCommandInteraction, guild_id: str):
    guild_appcom = self.__get_guild_appcom(interaction_obj.data.name, guild_id)
    if guild_appcom is None: return
    exe_infos = get_appcom_exedata(interaction_obj.data.options, guild_appcom._get_functions())
    await exe_infos.func(interaction_obj, self.appcom_resources, exe_infos.args)

  async def __interaction_exe_application_command(self, event_data: dict[str, Any]):
    event_obj = self.load_object(recv_event_object.ApplicationCommandInteraction, event_data)
    if event_obj is None: return
    if event_obj.data.guild_id is None:
      await self.__execution_global_application_command(event_obj)
    else:
      await self.__execution_guild_application_command(event_obj, event_obj.data.guild_id)
  #####################################

  ### message component execution ###
  async def __interaction_exe_message_component(self, event_data: dict[str, Any]):
    event_obj = self.load_object(recv_event_object.MessageComponentInteraction, event_data)
  ###################################

  ### application command autocomplete execution ###
  #TODO name_localizationの対応
  async def __send_autocomplete_callback(self, data: dict[str, str|int|float], interaction_id: str, interaction_token: str):
    req_list = b_interaction.InteractionCallbackAutocomplete([b_interaction.ACChoiceOption(k, v) for k, v in data.items()])
    req_data = self.httpapi.loader.load_request(
      b_interaction.CreateInteractionResponse(
        b_interaction.CT_APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
        data=req_list
      ),
      interaction_id=interaction_id,
      interaction_token=interaction_token
    )
    await self.httpapi.request.add_request(req_data)

  async def __global_autocomplete(self, interaction_obj: recv_event_object.ApplicationCommandAutocompleteInteraction):
    global_appcom = self.__get_global_appcom(interaction_obj.data.name)
    if global_appcom is None: return
    autocomplete_func = get_autocomplete_func(interaction_obj.data.options, global_appcom._get_functions())
    data_dict = await autocomplete_func(interaction_obj, self.appcom_resources)
    await self.__send_autocomplete_callback(data_dict, interaction_obj.id, interaction_obj.token)

  async def __guild_autocomplete(self, interaction_obj: recv_event_object.ApplicationCommandAutocompleteInteraction, guild_id: str):
    guild_appcom = self.__get_guild_appcom(interaction_obj.data.name, guild_id)
    if guild_appcom is None: return
    autocomplete_func = get_autocomplete_func(interaction_obj.data.options, guild_appcom._get_functions())
    data_dict = await autocomplete_func(interaction_obj, self.appcom_resources)
    await self.__send_autocomplete_callback(data_dict, interaction_obj.id, interaction_obj.token)

  async def __interaction_exe_application_command_autocomplete(self, event_data: dict[str, Any]):
    event_obj = self.load_object(recv_event_object.ApplicationCommandAutocompleteInteraction, event_data)
    if event_obj is None: return
    if event_obj.data.guild_id is None:
      await self.__global_autocomplete(event_obj)
    else:
      await self.__guild_autocomplete(event_obj, event_obj.data.guild_id)
  ##################################################

  ### modul submit execution ###
  async def __interaction_exe_modul_submit(self, event_data: dict[str, Any]):
    event_obj = self.load_object(recv_event_object.ModulSubmitInteraction, event_data)
  ##############################

  async def interaction(self, event_data: dict[str, Any]):
    IT_PING = 1
    IT_APPLICATION_COMMNAND = 2
    IT_MESSAGE_COMPONENT = 3
    IT_APPLICATION_COMMAND_AUTOCOMPLETE = 4
    IT_MODUL_SUBMIT = 5
    type_functions = {
      IT_PING: self.__interaction_exe_ping,
      IT_APPLICATION_COMMNAND: self.__interaction_exe_application_command,
      IT_MESSAGE_COMPONENT: self.__interaction_exe_message_component,
      IT_APPLICATION_COMMAND_AUTOCOMPLETE: self.__interaction_exe_application_command_autocomplete,
      IT_MODUL_SUBMIT: self.__interaction_exe_modul_submit
    }

    interaction_type: int = event_data["type"]
    await type_functions[interaction_type](event_data)