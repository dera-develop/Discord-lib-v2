from discord_lib2.command.application_command import GuildApplicationCommand

def __list_l1_check(server_data: dict, client_data: dict, check_name: str) -> bool | None:
  client_ld = client_data.get(check_name)
  server_ld = server_data.get(check_name)
  if (client_ld is not None) and (server_ld is not None):
    try:
      client_ld_set = {d for d in client_ld}
      server_ld_set = {d for d in server_ld}
    except:
      return False
    if client_ld_set != server_ld_set:
      return True
  elif client_ld != server_ld:
    return True
  return None

def __options_check(server_options: list, client_options: list) -> bool:
  if len(server_options) != len(client_options):
    return True
  for client_option in client_options:
    defined = False
    check_client = {}
    check_server = {}
    for server_option in server_options:
      if (client_option.get("type") == server_option.get("type")) and (client_option.get("name") == server_option.get("name")):
        defined = True
        check_client = client_option
        check_server = server_option
        break
    if not defined:
      return True
    else:
      # option key check
      check_keys = [
        "description",
        "description_localizations",
        "name_localizations",
        "min_value",
        "max_value",
        "min_length",
        "max_length",
        "autocomplete"
      ]
      for check_key in check_keys:
        if check_client.get(check_key) != check_server.get(check_key):
          return True
      # required
      client_required = check_client.get("required")
      server_required = check_server.get("required")
      if client_required != server_required:
        return not((server_required is None) and (not client_required))
      # choices
      check_client_choices = check_client.get("choices")
      check_server_choices = check_server.get("choices")
      if check_client_choices is not None and check_server_choices is not None:
        try:
          check_client_choices_set = {frozenset(arg.items()) for arg in check_server_choices}
          check_server_choices_set = {frozenset(arg.items()) for arg in check_client_choices}
        except:
          return False
        if check_server_choices_set != check_client_choices_set:
          return True
      elif check_client_choices != check_server_choices:
        return True
      # channel_types
      rs = __list_l1_check(check_server, check_client, "channel_types")
      if rs is not None:
        return rs
      # file_types
      rs = __list_l1_check(check_server, check_client, "file_types")
      if rs is not None:
        return rs
      
      check_client_options = check_client.get("options")
      check_server_options = check_server.get("options")
      if not isinstance(check_client_options, list):
        return False
      if not isinstance(check_server_options, list):
        return False
      if __options_check(check_server_options, check_client_options):
        return True
  return False

def __set_client_data(client_data: dict, key_name: str, target_dict: dict):
  if key_name in client_data:
    target_dict[key_name] = client_data.get(key_name)

def __checker(server_data: dict, client_data: dict) -> dict:
  return_dict = {}
  check_keys = [
    "name_localizations",
    "description",
    "description_localizations",
    "default_member_permissions",
    "dm_permission",  # global
    "default_permission",
    "nsfw",
    "handler"         # global
  ]
  for k in check_keys:
    if client_data.get(k) != server_data.get(k):
      __set_client_data(client_data, k, return_dict)

  # integration_types
  rs = __list_l1_check(server_data, client_data, "integration_types")
  if rs:
    __set_client_data(client_data, "integration_types", return_dict)
  # contexts
  rs = __list_l1_check(server_data, client_data, "contexts")
  if rs:
    __set_client_data(client_data, "contexts", return_dict)

  # options
  server_options = server_data.get("options")
  client_options = client_data.get("options")
  if not isinstance(server_options, list):
    return return_dict
  if not isinstance(client_options, list):
    return return_dict
  if __options_check(server_options, client_options):
    __set_client_data(client_data, "options", return_dict)
  return return_dict

def __applicationcommand_set_namekey(datas) -> dict:
  return_dict = {}
  for data in datas:
    return_dict[data["name"]] = data
  return return_dict


def checker_v2(server_appcom_datas: list, client_appcom_datas: list) -> list:
  '''
  [
    { # create
      "data": <application_command_dict>,
      "new": true
    },
    { # edit
      "data": <application_command_dict>,
      "id": <command_id>,
      "edit": true
    },
    {
      "id": <command_id>,
      "del": true
    }
  ]
  '''
  change_datas = []
  server_datas = __applicationcommand_set_namekey(server_appcom_datas)
  server_datas_names = [name for name in server_datas.keys()]

  for command_data in client_appcom_datas:
    if not isinstance(command_data, GuildApplicationCommand):
      raise TypeError()

    # difference check
    data_dict = command_data._get()
    server_data = server_datas.get(data_dict["name"])
    if data_dict["name"] in server_datas_names:
      server_datas_names.remove(data_dict["name"])
    if server_data is None:
      # create
      change_datas.append({"data": data_dict, "new": True})
    else:
      # edit
      diff = __checker(server_data, data_dict)
      if diff != {}:
        change_datas.append({"data": diff, "id": data_dict["id"], "edit": True})
  for name in server_datas_names:
    change_datas.append({"id": server_datas[name]["id"], "del": True})
  return change_datas