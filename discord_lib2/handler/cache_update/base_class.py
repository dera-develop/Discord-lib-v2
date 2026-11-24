import copy
from logging import Logger
from typing import Callable, Any

from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.network.http_request import http, request_loader
from discord_lib2.cache.user.base import UserCacheBase

class HTTPcontroller:
  def __init__(self, request_controller: http.HttpRequestController, request_loader: request_loader.RequestLoader) -> None:
    self.request = request_controller
    self.loader = request_loader

class CacheUpdateBase:
  event_functions: dict[str, Callable] = {}

  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, data_cache: DataCacheVault, http_controller: HTTPcontroller) -> None:
    self.logger = logger
    self.exception_catcher = exception_catcher
    self.data_cache = data_cache
    self.httpapi = http_controller

  def _update_cache_dict(self, update_data: dict[str, Any], target_cache: dict, class_type: type[UserCacheBase], regist_key: str|None, field_name: str|None=None, overwrite: bool=False):
    """
    ### キャッシュ更新処理
    指定キャッシュを更新または上書き

    :param update_data: 更新情報本体
    :param target_cache: キャッシュの更新対象辞書
    :param class_type: 更新キャッシュ型
    :param regist_key: 更新キャッシュキー
    :param overwrite: 強制初期化フラグ
    """
    if regist_key is None:  return
    if overwrite or regist_key not in target_cache:
      target_cache[regist_key] = class_type()
    if field_name is None:
      target_cache[regist_key].update(update_data)
    else:
      attr = getattr(target_cache[regist_key], field_name)
      attr.update(update_data)

  def _update_sync(self, update_datas: list[dict[str, Any]], target_cache: dict, class_type: type[UserCacheBase], regist_key_path: str, field_name: str|None=None, overwrite: bool=False):
    """
    ### キャッシュ一括更新処理
    _update_cache_dictを使用して一括更新

    :param update_datas: 更新情報本体（配列）
    :param target_cache: キャッシュの更新対象辞書
    :param class_type: 更新キャッシュ型
    :regist_key_name: 抽出登録キーのパス | "user.id"なら，update_datasの各要素の["user"]["id"]キーの要素がキャッシュの登録キーとなる
    """
    paths = regist_key_path.split(".")
    for update_data in update_datas:
      regist_key = copy.deepcopy(update_data)
      for path in paths:
        if not isinstance(regist_key, dict): break
        regist_key = regist_key.get(path)
      if regist_key is None: continue
      if not isinstance(regist_key, str): continue
      self._update_cache_dict(update_data, target_cache, class_type, regist_key, field_name, overwrite)

  def _delete_cache_dict(self, target_cache: dict, target_key: str):
    """
    ### 対象キャッシュ削除
    対象のキャッシュを削除

    :param target_cache: キャッシュの更新対象辞書
    :param target_key: 削除するキャッシュのキー
    """
    if target_key in target_cache:
      target_cache.pop(target_key)

  def _add_cache_list(self, target_cache: list[str], add_key: str):
    """
    ### キャッシュ追加（1層配列）
    対象に値を追加（重複回避あり）

    :param target_cache: 値の追加対象配列
    :param add_key: 追加する値
    """
    if add_key not in target_cache:
      target_cache.append(add_key)

  def _delete_cache_list(self, target_cache: list[str], target_key: str):
    """
    ### 対象キャッシュ削除（1層配列）
    対象の値を削除

    :param target_cache: 値の削除対象配列
    :param target_key: 削除する値
    """
    if target_key in target_cache:
      target_cache.remove(target_key)

  def get_functions(self):
    return self.event_functions