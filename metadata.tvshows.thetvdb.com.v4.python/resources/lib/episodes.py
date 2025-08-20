from collections import defaultdict

import xbmcgui
import xbmcplugin
import json

from . import tvdb
from .nfo import parse_episode_guide_url
from .utils import logger, parse_unique_id, UniqueIdType, UniqueId
from .series import get_unique_ids, ARTWORK_URL_PREFIX


# add the episodes of a series to the list


def get_series_episodes(show_ids, settings, handle):
    logger.debug(f'Find episodes of tvshow with id {show_ids}')
    try:
        all_ids = json.loads(show_ids)
        unique_id = all_ids.get('tvdb')
        if not unique_id:
            unique_id = str(show_ids)
        unique_id = parse_unique_id(unique_id)
    except (ValueError, AttributeError):
        logger.warning('Loading episodes with unknown ID format, fallback')
        unique_id = str(show_ids)
        if unique_id.isdigit():
            logger.error(
                'using deprecated episodeguide format, this show should be refreshed or rescraped')
            unique_id = UniqueId(UniqueIdType.SERIES, unique_id)

    if not unique_id:
        raise RuntimeError(
            'No tvdb show id found in episode guide, this show should be refreshed or rescraped')
    elif unique_id is str:
        # Kodi has a bug: when a show directory contains an XML NFO file with
        # episodeguide URL, that URL is always passed here regardless of
        # the actual parsing result in get_show_id_from_nfo()
        parse_result = parse_episode_guide_url(unique_id)
        if not parse_result:
            return

        unique_id = UniqueId(UniqueIdType.SERIES, parse_result.show_id)
        logger.debug(f'Changed show id to {unique_id}')

    client = tvdb.Client(settings)

    if unique_id.id_type == UniqueIdType.SERIES:
        episodes = client.get_series_episodes_api(unique_id.tvdb_id, settings)
    elif unique_id.id_type == UniqueIdType.SEASON:
        episodes = client.get_season_episodes_api(unique_id.tvdb_id, settings)
    else:
        # Should not happen
        logger.error(f'Unsupported id {unique_id}')
        return

    if not episodes:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return

    for ep in episodes:
        liz = xbmcgui.ListItem(ep['name'], offscreen=True)
        details = {
            'title': ep['name'],
            'season': ep['seasonNumber'],
            'episode': ep['number'],
        }
        date_string = ep.get("aired")
        if date_string:
            year = int(date_string.split("-")[0])
            details['premiered'] = details['date'] = date_string
            details['year'] = year
            details['aired'] = ep['aired']
        logger.debug("details in episodes.py")
        logger.debug(details)
        liz.setInfo('video', details)
        xbmcplugin.addDirectoryItem(
            handle=handle, 
            url=str(UniqueId(UniqueIdType.EPISODE, ep['id'])),
            listitem=liz, 
            isFolder=True
            )

# get the details of the found episode
def get_episode_details(id, settings, handle):
    logger.debug(f'Find info of episode with id {id}')

    unique_id = parse_unique_id(id)
    if not unique_id:
        # backwards compatibility
        unique_id = UniqueId(UniqueIdType.EPISODE, id)

    client = tvdb.Client(settings)
    ep = client.get_episode_details_api(unique_id.tvdb_id, settings)
    if not ep:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return
    ep["uniqueId"] = unique_id

    liz = xbmcgui.ListItem(ep["name"], offscreen=True)
    cast = get_episode_cast(ep)
    rating = get_rating(ep)
    tags = get_tags(ep)
    duration_minutes = ep.get('runtime') or 0

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
        'duration': duration_minutes * 60,
    }

    if ep.get("airsAfterSeason"):
        details['sortseason'] = ep.get("airsAfterSeason")    
        details['sortepisode'] = 4096
    if ep.get("airsBeforeSeason"):
        details['sortseason'] = ep.get("airsBeforeSeason")
        details['sortepisode'] = 0
    if ep.get("airsBeforeEpisode"):
        details['sortepisode'] = ep.get("airsBeforeEpisode")
    if tags:
        details["tag"] = tags


    liz.setInfo('video', details)

    unique_ids = get_unique_ids(ep)
    liz.setUniqueIDs(unique_ids, 'tvdb')
    guest_stars = cast['guest_stars']
    if guest_stars:
        liz.setCast(guest_stars)
    if ep.get("image"):
        liz.addAvailableArtwork(ep["image"], 'thumb')
    xbmcplugin.setResolvedUrl(
        handle=handle, 
        succeeded=True,
        listitem=liz)


def get_episode_cast(ep):
    cast = defaultdict(list)
    characters = ep.get('characters')
    if characters:
        for char in characters:
            if char['peopleType'] == 'Writer':
                cast['writers'].append(char['personName'])
            elif char['peopleType'] == 'Director':
                cast['writers'].append(char['personName'])
            elif char['peopleType'] == 'Guest Star':
                person_info = {'name': char.get('personName') or ''}
                thumbnail = char.get('image') or char.get('personImgURL') or ''
                if thumbnail and not thumbnail.startswith(ARTWORK_URL_PREFIX):
                    thumbnail = ARTWORK_URL_PREFIX + thumbnail
                if thumbnail:
                    person_info['thumbnail'] = thumbnail
                cast['guest_stars'].append(person_info)
    return cast


def get_rating(ep):
    ratings = ep.get("contentRatings", [])
    rating = ''
    if len(ratings) == 1:
        rating = ratings[0]['country'] + ': ' + ratings[0]["name"]
    if not rating:
        for r in ratings:
            if r["country"] == "usa":
                rating = 'USA: ' + r["name"]
    return rating


def get_tags(ep):
    tags = []
    tag_options = ep.get("tagOptions", [])
    if tag_options:
        for tag in tag_options:
            tags.append(tag["name"])
    return tags
