#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import os.path
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import xbmc
import xbmcaddon
import xbmcplugin

from .artwork import get_artworks
from .episodes import get_episode_details, get_series_episodes
# from .artwork import get_artworks
from .nfo import get_show_id_from_nfo
from .series import get_series_details, search_series
from .utils import create_uuid, logger

# import episodes


ADDON_SETTINGS = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
images_url = 'http://thetvdb.com/banners/'

def run():
    qs = sys.argv[2][1:]
    params = dict(urllib.parse.parse_qsl(qs))
    logger.debug("THE TVDB ADDON")
    logger.debug(params)

    _action = params.get("action", "")
    action = urllib.parse.unquote_plus(_action)
    _settings = params.get("pathSettings", "{}")
    settings = json.loads(_settings)
    _title = params.get("title", "")
    title = urllib.parse.unquote_plus(_title)
    year = params.get("year", None)

    uuid = settings.get("uuid", None)
    if not uuid or uuid == "":
        uuid = create_uuid()
        ADDON_SETTINGS.setSetting("uuid", uuid)
        settings["uuid"] = uuid


    logger.debug("settings:")
    logger.debug(settings)
    if 'action' in params:
        if action == 'find' and title is not None:
            logger.debug("about to call search series")
            search_series(title, settings, HANDLE, year)
        elif action == 'getdetails' and 'url' in params:
            logger.debug("about to call get series details")
            get_series_details(
                urllib.parse.unquote_plus(params["url"]), settings, HANDLE)
        elif action == 'getepisodelist' and 'url' in params:
            logger.debug("about to call get series episodes")

            get_series_episodes(
                urllib.parse.unquote_plus(params["url"]), settings, HANDLE)
        elif action == 'getepisodedetails' and 'url' in params:
            logger.debug("about to call get episode details")
            get_episode_details(
                urllib.parse.unquote_plus(params["url"]), settings, HANDLE)
        elif action == 'getartwork' and 'id' in params:
            logger.debug("about to call get artworks")
            get_artworks(urllib.parse.unquote_plus(
                params["id"]), images_url, settings, HANDLE)
        elif params['action'].lower() == 'nfourl':
            logger.debug('performing nfourl action')
            get_show_id_from_nfo(params['nfo'])
    xbmcplugin.endOfDirectory(HANDLE)