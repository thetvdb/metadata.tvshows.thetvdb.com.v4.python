import xbmcgui
import xbmcplugin

from .tvdb import client, get_artworks_from_show, get_language

ART_LENGTH = 10


def add_artworks(show, liz, language):
    
    artworks = get_artworks_from_show(show, language)
    posters = artworks.get("posters", [])[:ART_LENGTH]
    banners = artworks.get("banners", [])[:ART_LENGTH]
    fanarts = artworks.get("fanarts", [])[:ART_LENGTH]
    season_posters = artworks.get("season_posters", [])

    for poster in posters:
        liz.addAvailableArtwork(poster["image"], 'poster')

    for banner in banners:
        liz.addAvailableArtwork(banner["image"], 'banner')

    for (image, season_number) in season_posters:
        liz.addAvailableArtwork(image, 'poster', season=season_number)

    fanart_items = []
    for fanart in fanarts:
        fanart_items.append(
            {'image': fanart["image"], 'preview': fanart["thumbnail"]})
    liz.setAvailableFanart(fanart_items)


def get_artworks(id, settings, handle):
    tvdb_client = client(settings)

    show = tvdb_client.get_series_details_api(id, settings)
    if not show:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(id, offscreen=True)
    language = get_language(settings)
    add_artworks(show, liz, language)
    xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=liz)
