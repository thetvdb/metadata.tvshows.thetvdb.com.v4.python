import unittest
import json
import sys
import urllib

from resources.lib import tvdb, simple_requests

class TestEpisodesApi(unittest.TestCase):
    def setUp(self):
        self.settings = {
            'gender': 'Other', 
            'language': 'English', 
            'pin': '', 
            'season_type': '1', 
            'uuid': '9b77c109-7700-4746-89b8-eb698970a25c', 
            'year': 1900
        }

        self.tvdb = tvdb.Client(self.settings)

    def test_get_episode_details_api_successfull_eng_translation(self):
        ep = self.tvdb.get_episode_details_api(id=9192947, settings=self.settings)

        self.assertEqual(9192947, ep['id'])
        self.assertEqual(418264, ep['seriesId'])


    def test_get_episode_details_api_successfull_other_lang_translation(self):
        custom_settings = self.settings.copy()
        custom_settings['language'] = 'Japanese'

        ep = self.tvdb.get_episode_details_api(id=9192947, settings=custom_settings)

        self.assertEqual(9192947, ep['id'])
        self.assertEqual(418264, ep['seriesId'])
        self.assertEqual('完結〜私の最終決断!!父娘愛が起こす奇跡', ep['name'], 'Episode title does not match.')

    
    def test_get_episode_details_api_fails_gracefully(self):
        """Expects None is returned. No unhandled exceptions are expected."""
        ep = self.tvdb.get_episode_details_api(id=9999999999999, settings=self.settings)
        ep = self.assertIsNone(ep)


if __name__ == '__main__':
    unittest.main()