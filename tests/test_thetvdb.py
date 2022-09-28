import unittest
import json
import sys
from unittest.mock import DEFAULT
import urllib

import importlib.machinery
loader = importlib.machinery.SourceFileLoader('resources', './metadata.tvshows.thetvdb.com.v4.python/resources/__init__.py')
resources = loader.load_module()

from resources.lib import tvdb, simple_requests

DEFAULT_SETTINGS = {
    'gender': 'Other', 
    'language': 'English', 
    'pin': '', 
    'season_type': '1', 
    'uuid': '9b77c109-7700-4746-89b8-eb698970a25c', 
    'year': 1900
}

class TestEpisodesApi(unittest.TestCase):
    def setUp(self):
        self.tvdb = tvdb.Client(DEFAULT_SETTINGS)

    def test_get_episode_details_api_successfull_eng_translation(self):
        ep = self.tvdb.get_episode_details_api(id=9192947, settings=DEFAULT_SETTINGS)

        self.assertEqual(9192947, ep['id'])
        self.assertEqual(418264, ep['seriesId'])


    def test_get_episode_details_api_successfull_other_lang_translation(self):
        custom_settings = DEFAULT_SETTINGS.copy()
        custom_settings['language'] = 'Japanese'

        ep = self.tvdb.get_episode_details_api(id=9192947, settings=custom_settings)

        self.assertEqual(9192947, ep['id'])
        self.assertEqual(418264, ep['seriesId'])
        self.assertEqual('完結〜私の最終決断!!父娘愛が起こす奇跡', ep['name'], 'Episode title does not match.')


    def test_get_episode_with_no_name_or_overview_on_primary_language(self):
        pass #TODO: find a sample on this situation


    def test_get_episode_details_api__no_english_translation(self):
        custom_settings = DEFAULT_SETTINGS.copy()

        custom_settings['language'] = 'English'
        ep = self.tvdb.get_episode_details_api(id=6490674, settings=custom_settings)
        self.assertIsNone(ep)

        custom_settings['language'] = 'German'
        ep = self.tvdb.get_episode_details_api(id=6490674, settings=custom_settings)
        self.assertEqual(6490674, ep['id'])
        self.assertEqual(273716, ep['seriesId'])
        self.assertEqual('Der Zirkus-Check', ep['name'], 'Episode title does not match.')

    def test_get_episode_details_api_fails_gracefully(self):
        """Expects None is returned. No unhandled exceptions are expected."""
        ep = self.tvdb.get_episode_details_api(id=9999999999999, settings=DEFAULT_SETTINGS)
        ep = self.assertIsNone(ep)

class TestSeriesApi(unittest.TestCase):
    def setUp(self):
        self.tvdb = tvdb.Client(DEFAULT_SETTINGS)

    def test_get_series_details_api_successfull_no_english_translation(self):
        series_info = self.tvdb.get_series_details_api(id=273716, settings=DEFAULT_SETTINGS)

        self.assertEqual(273716, series_info['id'])
        self.assertEqual('Checker Tobi', series_info['name'], 'Episode title does not match.')
        self.assertTrue(len(series_info['seasons']) > 0)


    def test_get_series_details_api_successfull_translated(self):
        custom_settings = DEFAULT_SETTINGS.copy()
        custom_settings['language'] = 'German'
        series_info = self.tvdb.get_series_details_api(id=273716, settings=custom_settings)

        self.assertEqual(273716, series_info['id'])
        self.assertEqual('Checker Tobi', series_info['name'], 'Episode title does not match.')
        self.assertTrue( series_info['overview'].startswith('Spin-off von Checker Can.') )
        self.assertTrue(len(series_info['seasons']) > 0)

if __name__ == '__main__':
    unittest.main()