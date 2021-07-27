#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

import xbmcgui
import xbmcplugin

from . import tvdb
from .artwork import add_artworks
from .utils import logger


def search_series(title, settings, handle, year=None) -> None:
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
            handle=handle,
            url=str(show['tvdb_id']),
            listitem=liz,
            isFolder=True
        )


def get_series_details(id, settings, handle):
    # get the details of the found series
    logger.debug(f'Find info of tvshow with id {id}')
    tvdb_client = tvdb.client(settings)

    show = tvdb_client.get_series_details_api(id, settings,)
    if not show:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(show["name"], offscreen=True)

    year_str = show.get("first_aired", "")
    year = None
    if year_str != "":
        year = int(year.split("-")[0])
    details = {'title': show["name"],
                'tvshowtitle': show["name"],
                'plot': show["overview"],
                'plotoutline': show["overview"],
                'episodeguide': show["id"],
                'mediatype': 'tvshow'
                }
    if year:
        details["year"] = year
        details["premiered"] = show["first_aired"]
    logger.debug(details)
    liz.setInfo('video', details
  )
    set_cast(liz, show)
    liz.setUniqueIDs({'tvdb': show["id"]}, 'tvdb')

    add_artworks(show, liz)
    xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=liz)


def set_cast(liz, show):
    cast = []
    for char in show["characters"]:
        if char["peopleType"] == "Actor":
            d = {}
            d["name"] = char["personName"]
            d["role"] = char["name"]
            cast.append(d)
    liz.setCast(cast)
    return
