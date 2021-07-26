#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

import xbmcgui
import xbmcplugin

from .tvdb import client, get_artworks_from_show

HANDLE = int(sys.argv[1])


def add_artworks(show, liz):
    
    artworks = get_artworks_from_show(show)
    posters = artworks.get("posters", [])
    banners = artworks.get("banners", [])
    fanarts = artworks.get("fanarts", [])
    season_posters = artworks.get("season_posters", [])



    for poster in posters:
        liz.addAvailableArtwork(poster["image"], 'poster')

    for banner in banners:
        liz.addAvailableArtwork(poster["image"], 'banner')

    for (image, season_number) in season_posters:
        liz.addAvailableArtwork(image, 'poster', season=season_number)

    fanart_items = []
    for fanart in fanarts:
        fanart_items.append(
            {'image': fanart["image"], 'preview': fanart["thumbnail"]})
    if fanarts:
        liz.setAvailableFanart(fanarts)


def get_artworks(id, images_url: str, settings):
    tvdb_client = client(settings)

    show = tvdb_client.get_series_details_api(id, settings)
    if not show:
        xbmcplugin.setResolvedUrl(
            HANDLE, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(id, offscreen=True)
    add_artworks(show, liz)
    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=liz)
