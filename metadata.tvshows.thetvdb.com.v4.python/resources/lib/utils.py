import uuid
from enum import StrEnum

import xbmc
from xbmcaddon import Addon

ADDON = Addon()
ADDON_ID = ADDON.getAddonInfo('id')


class logger:
    log_message_prefix = '[{} ({})]: '.format(
        ADDON_ID, ADDON.getAddonInfo('version'))

    @staticmethod
    def log(message, level=xbmc.LOGDEBUG):
        message = logger.log_message_prefix + str(message)
        xbmc.log(message, level)

    @staticmethod
    def info(message):
        logger.log(message, xbmc.LOGINFO)

    @staticmethod
    def error(message):
        logger.log(message, xbmc.LOGERROR)

    @staticmethod
    def debug(*messages):
        for message in messages:
            logger.log(message, xbmc.LOGDEBUG)

    @staticmethod
    def warning(message):
        logger.log(message, xbmc.LOGWARNING)


def create_uuid():
    return str(uuid.uuid4())

# The types of the objects which are loaded from the API.
class UniqueIdType(StrEnum):
    SERIES = 'series'
    SEASON = 'season'
    EPISODE = 'episode'

# NOTE: We would use '-', but currently Kodi doesn't allow using dashes in the filename identifiers.
# See: https://github.com/xbmc/xbmc/blob/1a346a7282f7e0ae2effb448f39bd4f4bbb74449/xbmc/settings/AdvancedSettings.cpp#L192
UNIQUE_ID_SEPARATOR = '_'

# A unique ID of an API object identifying its type and the numeric ID
class UniqueId:
    id_type: UniqueIdType
    tvdb_id: str

    def __init__(self, id_type: UniqueIdType, tvdb_id: str):
        self.id_type = id_type
        self.tvdb_id = tvdb_id

    def __str__(self):
        return f'{self.id_type}{UNIQUE_ID_SEPARATOR}{self.tvdb_id}'

# Parses a unique ID from the provided string
def parse_unique_id(unique_id: str) -> UniqueId | None:
    id_type = UniqueIdType.SERIES
    separator_index = unique_id.find(UNIQUE_ID_SEPARATOR)
    if separator_index == -1:
        tvdb_id = unique_id
    else:
        id_type = unique_id[:separator_index]
        tvdb_id = unique_id[(separator_index + 1):]

    try:
        id_type = UniqueIdType(id_type)
    except ValueError:
        return None

    return UniqueId(id_type, tvdb_id)
