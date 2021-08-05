from __future__ import absolute_import, unicode_literals

import uuid

import xbmc
from xbmcaddon import Addon

ADDON_ID = 'metadata.tvshows.thetvdb.v4.python'
ADDON = Addon()


class logger:
    log_message_prefix = '[{} ({})]: '.format(
        ADDON_ID, ADDON.getAddonInfo('version'))

    @staticmethod
    def log(message, level=xbmc.LOGDEBUG):
        if isinstance(message, bytes):
            message = message.decode('utf-8')
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


def create_uuid():
    return str(uuid.uuid4())
