import unittest
import json
import sys
from unittest.mock import DEFAULT
import urllib

import importlib.machinery
loader = importlib.machinery.SourceFileLoader('resources', './metadata.tvshows.thetvdb.com.v4.python/resources/__init__.py')
resources = loader.load_module()

from resources.lib import tvdb, series, episodes

DEFAULT_SETTINGS = {
    'gender': 'Other', 
    'language': 'English', 
    'pin': '', 
    'season_type': '1', 
    'uuid': '9b77c109-7700-4746-89b8-eb698970a25c', 
    'year': 1900
}

class TestSeries(unittest.TestCase):

    def test_search_series(self):
        # action == 'find'
        settings = DEFAULT_SETTINGS
        series.search_series('AEW Dark', settings, None, None)
        # only asserts it will not launch any exception. 
        # This search_series function/procedure currently doesn't returns a value
        #FIXME: improve the target function/procedure be testable!
        pass

    def test_series_details(self):
        # action == 'getdetails'
        #TODO
        pass


class TestEpisodes(unittest.TestCase):

    def test_get_series_episodes(self):
        # action == 'getepisodelist'
        #TODO
        id = 370561 #'AEW Dark'
        episodes.get_series_episodes(str(id), DEFAULT_SETTINGS, None)
        #FIXME: improve the target function/procedure to be testable!

    def test_get_episode_details(self):
        # action == 'getepisodedetails'
        """
        2022-09-15 20:11:44.523 T:18884   DEBUG <general>: [metadata.tvshows.thetvdb.com.v4.python (1.1.0)]: {'title': 'AEW Dark 160', 'season': 4, 'episode': 38, 'premiered': '2022-09-06', 'date': '2022-09-06', 'year': 2022}
        2022-09-15 20:11:44.523 T:18884   DEBUG <general>: [metadata.tvshows.thetvdb.com.v4.python (1.1.0)]: details in episodes.py
        2022-09-15 20:11:44.523 T:18884   DEBUG <general>: [metadata.tvshows.thetvdb.com.v4.python (1.1.0)]: {'title': 'AEW Dark 161', 'season': 4, 'episode': 39, 'premiered': '2022-09-13', 'date': '2022-09-13', 'year': 2022}
        """
        ep_id = 9351525 #'AEW Dark'
        episodes.get_episode_details(str(ep_id), DEFAULT_SETTINGS, None)
        pass


class TestNFO(unittest.TestCase):

    def test_get_show_id_from_nfo(self):
        #action == 'nfourl'
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()