import xbmcgui
import xbmcplugin

from . import tvdb
from .artwork import add_artworks
from .utils import logger

SUPPORTED_REMOTE_IDS = {
    'IMDB': 'imdb',
    'TheMovieDB.com': 'tmdb',
}


def search_series(title, settings, handle, year=None) -> None:
    # add the found shows to the list
    logger.debug(f'Searching for TV show "{title}"')

    tvdb_client = tvdb.client(settings)
    if year is None:
        search_results = tvdb_client.search(title, type="series", limit=10)
    else:
        search_results = tvdb_client.search(title, year=year, type="series", limit=10)
    logger.debug(f'Search results {search_results}')

    if search_results is None:
        return
    
    items = []
    for show in search_results: 
        nameAndYear = f"{show['name']}" if not show.get('year', None) else f"{show['name']} ({show['year']})"

        liz = xbmcgui.ListItem(nameAndYear, offscreen=True)
        url = str(show['tvdb_id'])
        is_folder = True
        items.append((url, liz, is_folder))

    xbmcplugin.addDirectoryItems(
        handle,
        items,
        len(items)
    )


def get_series_details(id, settings, handle):
    # get the details of the found series
    logger.debug(f'Find info of tvshow with id {id}')
    tvdb_client = tvdb.client(settings)

    show = tvdb_client.get_series_details_api(id, settings)
    if not show:
        xbmcplugin.setResolvedUrl(
            handle, False, xbmcgui.ListItem(offscreen=True))
        return

    year_str = show.get("firstAired", "")
    logger.debug("series year_str outside conditional")
    logger.debug(year_str)
    year = None
    if year_str:
        year = int(year_str.split("-")[0])
    details = {'title': show["name"],
                'tvshowtitle': show["name"],
                'plot': show["overview"],
                'plotoutline': show["overview"],
                'episodeguide': show["id"],
                'mediatype': 'tvshow',
                }
    if year:
        logger.debug("series year_str")
        logger.debug(year_str)
        details["premiered"] = year_str
    studio = get_studio(show)
    if studio:
        details["studio"] = studio
    genres = get_genres(show)
    details["genre"] = genres

    country = show.get("originalCountry", None)
    if country:
        details["country"] = country
    status = show.get('status')
    if status:
        details['status'] = status['name']
    name = show["name"]
    if year:
        name = f'{name} ({year})'
    liz = xbmcgui.ListItem(name, offscreen=True)

    logger.debug("series details", details)
    liz.setInfo('video', details)
    set_cast(liz, show)
    unique_ids = get_unique_ids(show)
    liz.setUniqueIDs(unique_ids, 'tvdb')

    add_artworks(show, liz)
    xbmcplugin.setResolvedUrl(
        handle=handle, 
        succeeded=True, 
        listitem=liz)


def set_cast(liz, show):
    cast = []
    for char in show["characters"]:
        if char["peopleType"] == "Actor":
            data = {
                'name': char['personName'],
                'role': char['name'],
            }
            thumbnail = char.get('image')
            if thumbnail:
                data['thumbnail'] = thumbnail
            cast.append(data)
    liz.setCast(cast)
    return


def get_genres(show):
    return [genre["name"] for genre in show.get("genres", [])]


def get_studio(show):
    companies = show.get("companies", [])
    if not companies:
        return None
    studio = None
    for company in companies:
        if company["primaryCompanyType"] == 1:
            studio = company["name"]
    if studio:
        return studio
    return companies[0]["name"]


def get_tags(show):
    tags = []
    tag_options = show.get("tagOptions", [])
    if tag_options:
        for tag in tag_options:
            tags.append(tag["name"])
    return tags


def get_unique_ids(show):
    unique_ids = {'tvdb': show['id']}
    remote_ids = show.get('remoteIds')
    if remote_ids:
        for remote_id_info in remote_ids:
            source_name = remote_id_info.get('sourceName')
            if source_name in SUPPORTED_REMOTE_IDS:
                unique_ids[SUPPORTED_REMOTE_IDS[source_name]] = remote_id_info['id']
    return unique_ids
