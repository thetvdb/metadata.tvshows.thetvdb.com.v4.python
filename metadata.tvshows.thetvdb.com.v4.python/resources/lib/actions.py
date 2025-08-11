import json
import sys
import urllib.error
import urllib.parse
import urllib.request

import xbmcplugin

from .artwork import get_artworks
from .episodes import get_episode_details, get_series_episodes
from .nfo import get_show_id_from_nfo
from .series import get_series_details, search_series
from .utils import create_uuid, logger, ADDON


def run():
    handle = int(sys.argv[1])
    qs = sys.argv[2][1:]
    params = dict(urllib.parse.parse_qsl(qs))
    logger.debug("THE TVDB TV SHOWS SCRAPER V.4")
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
        ADDON.setSetting("uuid", uuid)
        settings["uuid"] = uuid


    logger.debug("settings:")
    logger.debug(settings)
    if 'action' in params:
        if action == 'find' and title is not None:
            logger.debug("about to call search series")
            search_series(title, settings, handle, year)
        elif action == 'getdetails' and ('url' in params or 'uniqueIDs' in params):
            logger.debug("about to call get series details")
            _unique_ids = params.get("uniqueIDs", "{}")
            unique_ids = json.loads(_unique_ids)
            get_series_details(
                urllib.parse.unquote_plus(params.get("url") or ''), settings, handle, unique_ids)
        elif action == 'getepisodelist' and 'url' in params:
            logger.debug("about to call get series episodes")
            get_series_episodes(
                urllib.parse.unquote_plus(params["url"]), settings, handle)
        elif action == 'getepisodedetails' and 'url' in params:
            logger.debug("about to call get episode details")
            get_episode_details(
                urllib.parse.unquote_plus(params["url"]), settings, handle)
        elif action == 'getartwork' and 'id' in params:
            logger.debug("about to call get artworks")
            get_artworks(urllib.parse.unquote_plus(
                params["id"]), settings, handle)
        elif params['action'].lower() == 'nfourl':
            logger.debug('performing nfourl action')
            get_show_id_from_nfo(params['nfo'], settings, handle)
        else:
            logger.warning(f"unhandled action {action}")
    xbmcplugin.endOfDirectory(handle)
