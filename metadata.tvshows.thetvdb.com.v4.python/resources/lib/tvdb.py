#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import urllib
import urllib.parse
import urllib.request
from urllib.request import urlopen

from resources.lib.utils import logger

apikey = "1fb0f305-6011-4edd-a827-07440421fed9"
apikey_with_pin = "41080b3a-7506-478e-b616-2775663788b6"
class Auth:
    logger.debug("logging in")
    def __init__(self, url, apikey, pin="", **kwargs):
        loginInfo = {"apikey": apikey}
        if pin != "":
            loginInfo["pin"] = pin
            loginInfo["apikey"] = apikey_with_pin

        for key, value in kwargs.items():
            loginInfo[key] = value
        logger.debug("body in auth call")
        logger.debug(loginInfo)
        loginInfoBytes = json.dumps(loginInfo, indent=2).encode('utf-8')
        req = urllib.request.Request(url, data=loginInfoBytes)
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, data=loginInfoBytes) as response:
            res = json.load(response)
            self.token = res["data"]["token"]

    def get_token(self):
        return self.token


class Request:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.cache = {}

    def make_request(self, url):
        logger.debug("about to make request to url")
        logger.debug(url)
        data = self.cache.get(url, None)
        if data:
            return data

        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer {}".format(self.auth_token))
        with urllib.request.urlopen(req) as response:
            res = json.load(response)
            data = res["data"]
            self.cache[url] = data
            return data


class Url:
    def __init__(self):
        self.base_url = "https://api4.thetvdb.com/v4"

    def login_url(self):
        return "{}/login".format(self.base_url)

    def artwork_status_url(self):
        return "{}/artwork/statuses".format(self.base_url)

    def artwork_types_url(self):
        return "{}/artwork/types".format(self.base_url)

    def artwork_url(self, id, extended=False):
        url = "{}/artwork/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def awards_url(self, page):
        if page < 0:
            page = 0
        url = "{}/awards?page={}".format(self.base_url, page)
        return url

    def award_url(self, id, extended=False):
        url = "{}/awards/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def awards_categories_url(self):
        url = "{}/awards/categories".format(self.base_url)
        return url

    def award_category_url(self, id, extended=False):
        url = "{}/awards/categories/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def content_ratings_url(self):
        url = "{}/content/ratings".format(self.base_url)
        return url

    def countries_url(self):
        url = "{}/countries".format(self.base_url)
        return url

    def companies_url(self, page=0):
        url = "{}/companies?page={}".format(self.base_url, page)
        return url

    def company_url(self, id):
        url = "{}/companies/{}".format(self.base_url, id)
        return url

    def all_series_url(self, page=0):
        url = "{}/series".format(self.base_url)
        return url

    def series_url(self, id, extended=False):
        url = "{}/series/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def movies_url(self, page=0):
        url = "{}/movies".format(self.base_url, id)
        return url

    def movie_url(self, id, extended=False):
        url = "{}/movies/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def season_url(self, id, extended=False):
        url = "{}/seasons/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def episode_url(self, id, extended=False):
        url = "{}/episodes/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def episode_translation_url(self, id:int, language:str="eng"):
        url = "{}/episodes/{}/translations/{}".format(self.base_url, id, language)
        return url 

    def person_url(self, id, extended=False):
        url = "{}/people/{}".format(self.base_url, id)
        if extended:
            url = "{}/extended".format(url)
        return url

    def character_url(self, id):
        url = "{}/characters/{}".format(self.base_url, id)
        return url

    def people_types_url(self, id):
        url = "{}/people/types".format(self.base_url)
        return url

    def source_types_url(self):
        url = "{}/sources/types".format(self.base_url)
        return url

    def updates_url(self, since=0):
        url = "{}/updates?since={}".format(self.base_url, since)
        return url

    def tag_options_url(self):
        url = "{}/tags/options".format(self.base_url)
        return url

    def tag_option_url(self, id):
        url = "{}/tags/options/{}".format(self.base_url, id)
        return url

    def search_url(self, query, filters):
        filters["query"] = query
        qs = urllib.parse.urlencode(filters)
        url = "{}/search?{}".format(self.base_url, qs)
        return url

    def series_translation_url(self, id: int, language="eng"):
        url = "{}/series/{}/translations/{}".format(
            self.base_url, id, language)
        return url

    def series_season_episodes_url(self, id: int, season_type_number: int = 1, page: int = 0):
        season_type = "default"
        if season_type_number == 2:
            season_type = "absolute"
        if season_type_number == 3:
            season_type = "dvd"
        url = "{}/series/{}/episodes/{}?page={}".format(
            self.base_url, id, season_type, page)
        return url


class TVDB:
    def __init__(self, apikey: str, pin="", **kwargs):
        self.url = Url()
        login_url = self.url.login_url()
        self.auth = Auth(login_url, apikey, pin, **kwargs)
        auth_token = self.auth.get_token()
        self.request = Request(auth_token)

    def get_artwork_statuses(self) -> list:
        """Returns a list of artwork statuses"""
        url = self.url.artwork_status_url()
        return self.request.make_request(url)

    def get_artwork_types(self) -> list:
        """Returns a list of artwork types"""
        url = self.url.artwork_types_url()
        return self.request.make_request(url)

    def get_artwork(self, id: int) -> dict:
        """Returns an artwork dictionary"""
        url = self.url.artwork_url(id)
        return self.request.make_request(url)

    def get_artwork_extended(self, id: int) -> dict:
        """Returns an artwork extended dictionary"""
        url = self.url.artwork_url(id, True)
        return self.request.make_request(url)

    def get_all_awards(self, page=0) -> list:
        """Returns a list of awards"""
        url = self.url.awards_url(page)
        return self.request.make_request(url)

    def get_award(self, id: int) -> dict:
        """Returns an award dictionary"""
        url = self.url.award_url(id, False)
        return self.request.make_request(url)

    def get_award_extended(self, id: int) -> dict:
        """Returns an award extended dictionary"""
        url = self.url.award_url(id, True)
        return self.request.make_request(url)

    def get_all_award_categories(self) -> list:
        """Returns a list of award categories"""
        url = self.url.awards_categories_url()
        return self.request.make_request(url)

    def get_award_category(self, id: int) -> dict:
        """Returns an artwork category dictionary"""
        url = self.url.award_category_url(id, False)
        return self.request.make_request(url)

    def get_award_category_extended(self, id: int) -> dict:
        """Returns an award category extended dictionary"""
        url = self.url.award_category_url(id, True)
        return self.request.make_request(url)

    def get_content_ratings(self) -> list:
        """Returns a list of content ratings"""
        url = self.url.content_ratings_url()
        return self.request.make_request(url)

    def get_countries(self) -> list:
        """Returns a list of countries"""
        url = self.url.countries_url()
        return self.request.make_request(url)

    def get_all_companies(self, page=0) -> list:
        """Returns a list of companies"""
        url = self.url.companies_url(page)
        return self.request.make_request(url)

    def get_company(self, id: int) -> dict:
        """Returns a company dictionary"""
        url = self.url.company_url(id)
        return self.request.make_request(url)

    def get_all_series(self, page=0) -> list:
        """Returns a list of series"""
        url = self.url.all_series_url(page)
        return self.request.make_request(url)

    def get_series(self, id: int) -> dict:
        """Returns a series dictionary"""
        url = self.url.series_url(id, False)
        return self.request.make_request(url)

    def get_series_extended(self, id: int) -> dict:
        """Returns an series extended dictionary"""
        url = self.url.series_url(id, True)
        return self.request.make_request(url)

    def get_series_translation(self, id: int, lang: str) -> dict:
        """Returns a series translation dictionary"""
        url = self.url.series_translation_url(id, lang)
        return self.request.make_request(url)

    def get_all_movies(self, page=0) -> list:
        """Returns a list of movies"""
        url = self.url.movies_url(page)
        return self.request.make_request(url)

    def get_movie(self, id: int) -> dict:
        """Returns a movie dictionary"""
        url = self.url.movie_url(id, False)
        return self.request.make_request(url)

    def get_movie_extended(self, id: int) -> dict:
        """Returns a movie extended dictionary"""
        url = self.url.movie_url(id, True)
        return self.request.make_request(url)

    def get_movie_translation(self, lang: str) -> dict:
        """Returns a movie translation dictionary"""
        url = self.url.movie_translation_url(id, lang)
        return self.request.make_request(url)

    def get_season(self, id: int) -> dict:
        """Returns a season dictionary"""
        url = self.url.season_url(id, False)
        return self.request.make_request(url)

    def get_season_extended(self, id: int) -> dict:
        """Returns a season extended dictionary"""
        url = self.url.season_url(id, True)
        return self.request.make_request(url)

    def get_episode(self, id: int) -> dict:
        """Returns an episode dictionary"""
        url = self.url.episode_url(id, False)
        return self.request.make_request(url)

    def get_episode_translation(self, id: int, lang: str) -> dict:
        """Returns an episode translation dictionary"""
        url = self.url.episode_translation_url(id, lang)
        return self.request.make_request(url)

    def get_episode_extended(self, id: int) -> dict:
        """Returns an episode extended dictionary"""
        url = self.url.episode_url(id, True)
        return self.request.make_request(url)

    def get_person(self, id: int) -> dict:
        """Returns a person dictionary"""
        url = self.url.person_url(id, False)
        return self.request.make_request(url)

    def get_person_extended(self, id: int) -> dict:
        """Returns a person extended dictionary"""
        url = self.url.person_url(id, True)
        return self.request.make_request(url)

    def get_character(self, id: int) -> dict:
        """Returns a character dictionary"""
        url = self.url.character_url(id)
        return self.request.make_request(url)

    def get_all_people_types(self) -> list:
        """Returns a list of people types"""
        url = self.url.people_types_url()
        return self.request.make_request(url)

    def get_all_sourcetypes(self) -> list:
        """Returns a list of sourcetypes"""
        url = self.url.source_types_url()
        return self.request.make_request(url)

    def get_updates(self, since: int) -> list:
        """Returns a list of updates"""
        url = self.url.updates_url(since)
        return self.request.make_request(url)

    def get_all_tag_options(self, page=0) -> list:
        """Returns a list of tag options"""
        url = self.url.tag_options_url()
        return self.request.make_request(url)

    def get_tag_option(self, id: int) -> dict:
        """Returns a tag option dictionary"""
        url = self.url.tag_option_url(id)
        return self.request.make_request(url)

    def search(self, query, **kwargs) -> list:
        """Returns a list of search results"""
        url = self.url.search_url(query, kwargs)
        return self.request.make_request(url)

    def get_series_season_episodes(self, id: int, season_type: int = 1):
        page = 0
        episodes = []
        while True:
            url = self.url.series_season_episodes_url(id, season_type, page)
            res = self.request.make_request(url).get("episodes", [])
            page += 1
            if len(res) == 0:
                break
            episodes.extend(res)
        return episodes

    def get_series_details_api(self, id, settings=None) -> dict:
        settings = settings or {}
        series = self.get_series_extended(id)
        lang = get_language(settings)
        translations = None
        try:
            translations = self.get_series_translation(id, lang)
        except:
            translations = self.get_series_translation(id, "eng")
        overview = translations.get("overview", "")
        series["overview"] = overview
        name = translations.get("name", "")
        series["name"] = name
        return series

    def get_series_episodes_api(self, id, settings):
        season_type = get_season_type(settings)
        return self.get_series_season_episodes(id, season_type)

    def get_episode_details_api(self, id, settings):
        ep = self.get_episode_extended(id)
        lang = get_language(settings)
        trans = None
        try:
            trans = self.get_episode_translation(id, lang)
        except:
            trans = self.get_episode_translation(id, "eng")
        overview = trans.get("overview", "")
        ep["overview"] = overview
        name = trans.get("name", "")
        ep["name"] = name

        return ep

def get_language(settings):
    return settings.get("language", "eng")

def get_season_type(settings):
    season_type_str = settings.get("season_type", "1")
    return int(season_type_str)




class client(object):
    _instance = None

    def __new__(cls, settings=None):
        settings = settings or {}
        if cls._instance is None:
            pin = settings.get("pin", "")
            gender = settings.get("gender", "Other")
            uuid = settings.get("uuid", "")
            birth_year = settings.get("year", "")
            cls._instance = TVDB(apikey, pin=pin, gender=gender, birthYear=birth_year, uuid=uuid)
        return cls._instance

ARTWORK_TYPE_BANNER = 1
ARTWORK_TYPE_POSTER = 2
ARTWORK_TYPE_FANART = 3
ARTWORK_TYPE_SEASON_POSTER = 7


def get_artworks_from_show(show:dict):
    artworks = show.get("artworks", [{}])

    banners = sorted([art for art in artworks if art.get("type", 0) == ARTWORK_TYPE_BANNER], key=lambda image: image.get("score", 0),reverse=True)
    posters = sorted([art for art in artworks if art.get("type", 0) == ARTWORK_TYPE_POSTER], key=lambda image: image.get("score", 0),reverse=True)
    fanarts = sorted([art for art in artworks if art.get("type", 0) == ARTWORK_TYPE_FANART], key=lambda image: image.get("score", 0),reverse=True)
    season_posters = [(season.get("image", ""), season.get("number", 0)) for season in show.get("seasons", [])]
    artwork_dict = {
        "banners": banners,
        "posters": posters,
        "fanarts":fanarts,
        "season_posters": season_posters,
    }
    return artwork_dict
