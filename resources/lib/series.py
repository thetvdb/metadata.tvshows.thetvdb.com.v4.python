#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

import xbmcgui
import xbmcplugin

from . import tvdb
from .artwork import add_artworks
from .utils import logger

HANDLE = int(sys.argv[1])


def search_series(title, settings, year=None) -> None:
    # add the found shows to the list
    logger.debug(f'Searching for TV show "{title}"')

    tvdb_client = tvdb.client(settings)
    search_results = None
    if year is None:
        search_results = tvdb_client.search(title, type="series")
    else:
        search_results = tvdb_client.search(title, year=year, type="series")
    logger.debug(f'Search results {search_results}')

    if search_results is None:
        return
    for show in search_results:
        nameAndYear = f"{show['name']}" if not show[
            'year'] else f"{show['name']} ({show['year']})"

        liz = xbmcgui.ListItem(nameAndYear, offscreen=True)
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=str(show['tvdb_id']),
            listitem=liz,
            isFolder=True
        )


def get_series_details(id, settings):
    # get the details of the found series
    logger.debug(f'Find info of tvshow with id {id}')
    tvdb_client = tvdb.client(settings)

    show = tvdb_client.get_series_details_api(id, settings)
    if not show:
        xbmcplugin.setResolvedUrl(
            HANDLE, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(show["name"], offscreen=True)
    liz.setInfo('video',
                {'title': show["name"],
                 'tvshowtitle': show["name"],
                 'plot': show["overview"],
                 'plotoutline': show["overview"],
                 'episodeguide': show["id"],
                 'mediatype': 'tvshow'
                 })

    liz.setUniqueIDs({'tvdb': show["id"]}, 'tvdb')

    add_artworks(show, liz)
    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=liz)
