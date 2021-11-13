import pathlib
import sys
import unittest


project_dir = pathlib.Path('.').resolve().parent.parent
sys.path.append(str(project_dir))

from tvdb import TVDB, Client, get_artworks_from_show

apikey = "%apikey%"


class TestTVDB(unittest.TestCase):

    def test_login(self):
        try:
            TVDB(apikey)
        except Exception as e:
            self.assertIsNone(e)

    def test_search(self):
        api = TVDB(apikey)
        res = api.search("lost", type="series", year="2004", limit=10)
        first = res[0]
        self.assertEqual(first.get("name"), "Lost")
        self.assertEqual(first.get("tvdb_id"), "73739")

    def test_client(self):
        c1 = Client()
        c2 = Client()
        self.assertEqual(c1, c2)

    def test_get_series_details(self):
        c = Client()
        settings = {'language': 'English'}
        show = c.get_series_details_api(73739, settings)
        self.assertIsNotNone(show)
        overview = show.get("overview", None)
        self.assertIsNotNone(overview)
        self.assertNotEqual(overview, "")
        name = show.get("name", None)
        self.assertIsNotNone(name)
        self.assertNotEqual(name, "")
        self.assertEqual(name, "Lost")
        settings = {'language': 'Spanish'}
        show = c.get_series_details_api(73739, settings)
        self.assertIsNotNone(show)
        overview = show.get("overview", None)
        self.assertIsNotNone(overview)
        self.assertNotEqual(overview, "")
        name = show.get("name", None)
        self.assertIsNotNone(name)
        self.assertNotEqual(name, "")
        self.assertNotEqual(name, "Lost")
        self.assertEqual(name, "Perdidos")

    def test_get_series_episodes_api(self):
        c = Client()
        eps = c.get_series_episodes_api(
            121361, {})
        self.assertNotEqual(len(eps), 0)

    def test_get_artwork(self):
        c = Client()
        settings = {'language': 'English'}
        show = c.get_series_details_api(73739, settings)
        self.assertIsNotNone(show)
        artworks = get_artworks_from_show(show)
        self.assertIsNotNone(artworks)
        
        banners = artworks.get("banners", None)
        self.assertIsNotNone(banners)
        self.assertGreater(len(banners), 0)

        last_score = float('inf')
        for banner in banners:
            self.assertEqual(banner.get("type", 0), 1)
            score = banner.get("score", 0)
            self.assertLessEqual(score, last_score)
            last_score = score
        
        posters = artworks.get("posters", None)
        self.assertIsNotNone(posters)
        self.assertGreater(len(posters), 0)

        last_score = float('inf')
        for poster in posters:
            self.assertEqual(poster.get("type", 0), 2)
            score = poster.get("score", 0)
            self.assertLessEqual(score, last_score)
            last_score = score
    
    def test_get_episode_details_api(self):
        c = Client()
        ep = c.get_episode_details_api(3254641, {})
        self.assertIsNotNone(ep)

        overview = ep.get("overview", None)
        self.assertIsNotNone(overview)
        self.assertNotEqual(overview, "")

        name = ep.get("name", None)
        self.assertIsNotNone(name)
        self.assertNotEqual(name, "")

        image = ep.get("image", None)
        self.assertIsNotNone(image)
        self.assertNotEqual(image, "")


if __name__ == '__main__':
    unittest.main()
