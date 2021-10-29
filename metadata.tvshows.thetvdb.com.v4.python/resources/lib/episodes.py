import xbmcgui
import xbmcplugin

from . import tvdb
from .nfo import parse_episode_guide_url
from .utils import logger
from .series import get_unique_ids


# add the episodes of a series to the list


def get_series_episodes(id, settings, handle):
    logger.debug(f'Find episodes of tvshow with id {id}')
    if not id.isdigit():
        # Kodi has a bug: when a show directory contains an XML NFO file with
        # episodeguide URL, that URL is always passed here regardless of
        # the actual parsing result in get_show_id_from_nfo()
        parse_result = parse_episode_guide_url(id)
        if not parse_result:
            return

        if parse_result.provider == 'thetvdb':
            id = parse_result.show_id
            logger.debug(f'Changed show id to {id}')

    client = tvdb.client(settings)
    episodes = client.get_series_episodes_api(id, settings)

    if not episodes:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    for ep in episodes:
        liz = xbmcgui.ListItem(ep['name'], offscreen=True)
        year = None 
        year_str = ep.get("aired", "")
        if year_str:
            year = int(year_str.split("-")[0])

        details = {
            'title': ep['name'],
            'premiered': year_str,
            'date': year_str,
            "year": year,
            'season': ep['seasonNumber'],
            'episode': ep['number'],
        }
        logger.debug("details in episodes.py")
        logger.debug(details)
        liz.setInfo('video', details)
        xbmcplugin.addDirectoryItem(
            handle=handle, 
            url=str(ep['id']),
            listitem=liz, 
            isFolder=True
            )
    xbmcplugin.setResolvedUrl(
        handle=handle, 
        succeeded=True, 
        listitem=liz
        )

# get the details of the found episode


def get_episode_details(id, settings, handle):
    logger.debug(f'Find info of episode with id {id}')
    client = tvdb.client(settings)
    ep = client.get_episode_details_api(id, settings)
    if not ep:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    liz = xbmcgui.ListItem(ep["name"], offscreen=True)
    cast = get_episode_cast(ep)
    rating = get_rating(ep)
    tags = get_tags(ep)

    
    details = {
        'title': ep["name"],
        'plot': ep["overview"],
        'plotoutline': ep["overview"],
        'premiered': ep["aired"],
        'aired': ep["aired"],
        'mediatype': 'episode',
        'director': cast["directors"],
        'writer': cast["writers"],
        'mpaa': rating,
    }

    if tags:
        details["tag"] = tags

    logger.debug("details in get episode details")
    logger.debug(details)
    logger.debug(ep)
    liz.setInfo('video', details)

    unique_ids = get_unique_ids(ep)
    liz.setUniqueIDs(unique_ids, 'tvdb')

    if ep.get("image", "") != "":
        liz.addAvailableArtwork(ep["image"])
    xbmcplugin.setResolvedUrl(
        handle=handle, 
        succeeded=True, 
        listitem=liz)


def get_episode_cast(ep):
    cast = {}
    characters = ep.get("characters", None)
    if not characters:
        return {"writers": [], "directors": []}
    writers = [char["personName"] for char in ep.get("characters", []) if char["peopleType"] == "Writer"]   
    directors = [char["personName"] for char in ep.get("characters", []) if char["peopleType"] == "Director"]   

    cast["writers"] = writers
    cast["directors"] = directors
    return cast

def get_rating(ep):
    ratings = ep.get("contentRatings", [])
    rating = ""
    for r in ratings:
        if r["country"] == "usa":
            rating = r["name"]
    
    if rating == "" and len(ratings) != 0:
        rating = ratings[0]["name"]
    
    return rating

def get_tags(ep):
    tags = []
    tag_options = ep.get("tagOptions", [])
    if tag_options:
        for tag in tag_options:
            tags.append(tag["name"])
    return tags
