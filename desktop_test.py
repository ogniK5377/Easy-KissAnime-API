import unittest
from KissAnime import desktop
print 'Init KissAnime desktop'
KD = desktop.KissAnime()
KD_Results = None
KD_AList = None
KD_RAnime = None
KD_Nichijou = None


class TestConnectionHandler(unittest.TestCase):
    def test_info(self):
        self.assertTrue(KD.conn.is_initalized, "Failed to initialize")
        self.assertIsNotNone(KD.conn.scrape, "Desktop scraper failed")
        self.assertIsNotNone(KD.conn.mobile_scrape, "Mobile scraper failed")
        self.assertIsNotNone(KD.conn.cf_db, "Database failed")
        self.assertIsNotNone(KD.conn.cursor)
        for i in xrange(2):
            KD.conn.cursor.execute('''
            SELECT * FROM Cookies WHERE DomainID=%d
            ''' % i)
            self.assertIsNotNone(KD.conn.cursor.fetchone(),
                                 "Failed to fetch DomainID %d from db" % i)


@unittest.skipIf(KD.conn.is_initalized is False, "Connection not initialized")
class TestSearch(unittest.TestCase):
    def test_fetch(self):
        global KD_Results
        KD_Results = KD.search('Dragonball')
        self.assertGreater(KD_Results, 3)
        KD_Results = KD.search(keyword='Dragonball')
        self.assertGreater(KD_Results, 3)

    def test_info(self):
        self.assertIsNotNone(KD_Results, "Failed to fetch results")
        self.assertGreater(len(KD_Results), 0, "No results")
        self.assertTrue('dragonball' in
                        KD_Results[0].get_title().lower(),
                        "Incorrect title")
        self.assertTrue('http' in KD_Results[0].get_url(), "Incorrect URL")


@unittest.skipIf(KD.conn.is_initalized is False, "Connection not initialized")
class TestAnimeList(unittest.TestCase):
    def test_fetch(self):
        global KD_AList
        anime_list = KD.get_anime_list('A', 0)
        self.assertIsNotNone(anime_list, "Failed to fetch anime list")
        self.assertGreater(len(anime_list), 0, "No animes in anime list")

        anime_list = KD.get_anime_list(letter_filter='C', page=3)
        self.assertIsNotNone(anime_list, "Failed to fetch anime list")
        self.assertGreater(len(anime_list), 0, "No animes in anime list")

        KD_AList = KD.get_anime_list(letter_filter='#')
        self.assertIsNotNone(KD_AList, "Failed to fetch anime list")
        self.assertGreater(len(KD_AList), 0, "No animes in anime list")

    def test_info(self):
        global KD_AList
        self.assertIsNotNone(KD_AList, "Failed to fetch anime list")
        self.assertGreater(len(KD_AList), 0, "No animes in anime list")

        anime = KD_AList[0]
        self.assertIsNotNone(anime, "Failed to fetch anime")
        self.assertIsNotNone(anime.title, "Failed to fetch anime title")
        self.assertIsNotNone(anime.url, "Failed to fetch anime url")
        self.assertIsNotNone(anime.status, "Failed to fetch anime status")

        self.assertGreater(len(anime.title), 0, "Invalid title")
        self.assertGreater(len(anime.status), 0, "Invalid status")
        self.assertGreater(len(anime.url), 0, "Invalid url")
        self.assertTrue('http' in anime.url, "Invalid URL")
        self.assertLess(ord(anime.title[0]), ord('a'),
                        "Incorrect title placement")


@unittest.skipIf(KD.conn.is_initalized is False, "Connection not initialized")
class TestRandomAnime(unittest.TestCase):
    def test_fetch(self):
        global KD_RAnime
        random_anime = KD.get_random_anime(genre='Action',
                                           excluded_anime='Yu-Gi-Oh-Arc-V-Dub;\
                                           Black-Rock-Shooter-TV;')
        self.assertIsNotNone(random_anime)
        KD_RAnime = KD.get_random_anime(genre='Ecchi')
        self.assertIsNotNone(random_anime)

    def test_info(self):
        global KD_RAnime
        self.assertIsNotNone(KD_RAnime, "Failed to fetch anime")
        anime = KD_RAnime
        self.assertIsNotNone(anime, "Failed to fetch anime")
        self.assertIsNotNone(anime.title, "Failed to fetch anime title")
        self.assertIsNotNone(anime.url, "Failed to fetch anime url")
        self.assertIsNotNone(anime.tags, "Failed to fetch anime tags")
        self.assertIsNotNone(anime.description,
                             "Failed to fetch anime description")
        self.assertGreater(len(anime.title), 0, "Invalid title")
        self.assertGreater(len(anime.url), 0, "Invalid status")
        self.assertGreater(len(anime.tags), 0, "Invalid url")
        self.assertTrue('http' in anime.url, "Invalid URL")
        self.assertTrue(isinstance(anime.description, basestring),
                        "Invalid description")
        # Description can be empty


@unittest.skipIf(KD.conn.is_initalized is False, "Connection not initialized")
class TestAnimeInfo(unittest.TestCase):
    def test_fetch(self):
        global KD_Nichijou
        r_anime = KD.get_random_anime()
        self.assertIsNotNone(r_anime, "Failed to fetch random anime")
        anime = KD.get_anime_info(r_anime)
        self.assertIsNotNone(anime, "Failed to fetch anime")
        self.assertIsNotNone(anime.title, "Failed to fetch anime title")
        self.assertIsNotNone(anime.other_names,
                             "Failed to fetch anime alterative names")
        self.assertIsNotNone(anime.tags, "Failed to fetch anime tags")
        self.assertIsNotNone(anime.air_date, "Failed to fetch anime air_date")
        self.assertIsNotNone(anime.status, "Failed to fetch anime status")
        self.assertIsNotNone(anime.views, "Failed to fetch anime views")
        self.assertIsNotNone(anime.summary, "Failed to fetch anime summary")
        self.assertIsNotNone(anime.episodes, "Failed to fetch anime episodes")

        KD_Nichijou = KD.get_anime_info(
            desktop.BASE_URL + 'Anime/Nichijou'
        )

    def test_info(self):
        global KD_Nichijou
        anime = KD_Nichijou
        self.assertIsNotNone(anime, "Failed to fetch anime")
        self.assertIsNotNone(anime.title, "Failed to fetch anime title")
        self.assertIsNotNone(anime.other_names,
                             "Failed to fetch anime alterative names")
        self.assertIsNotNone(anime.tags, "Failed to fetch anime tags")
        self.assertIsNotNone(anime.air_date, "Failed to fetch anime air_date")
        self.assertIsNotNone(anime.status, "Failed to fetch anime status")
        self.assertIsNotNone(anime.views, "Failed to fetch anime views")
        self.assertIsNotNone(anime.summary, "Failed to fetch anime summary")
        self.assertIsNotNone(anime.episodes, "Failed to fetch anime episodes")

        self.assertGreater(len(anime.title), 0, "Invalid title")
        self.assertGreater(len(anime.other_names), 0, "Invalid alt names")
        self.assertGreater(len(anime.tags), 0, "Invalid tags")
        self.assertGreater(len(anime.air_date), 0, "Invalid air_date")
        self.assertGreater(len(anime.status), 0, "Invalid status")
        self.assertGreater(len(anime.views), 0, "Invalid views")
        self.assertGreater(len(anime.summary), 0, "Invalid summary")
        self.assertGreater(len(anime.episodes), 0, "Invalid episodes")

        episode = anime.episodes[0]
        self.assertIsNotNone(episode.title, "Failed to fetch ep title")
        self.assertIsNotNone(episode.url, "Failed to fetch ep url")
        self.assertIsNotNone(episode.date, "Failed to fetch ep date")
        self.assertGreater(len(episode.title), 0, "Invalid title")
        self.assertGreater(len(episode.url), 0, "Invalid url")
        self.assertGreater(len(episode.date), 0, "Invalid date")
        self.assertTrue('http' in episode.url, "Invalid URL")

        ep_info = KD.get_anime_episode(episode)
        self.assertGreater(len(ep_info), 0, "Invalid url")
        self.assertTrue('http' in ep_info, "Invalid URL")

        ep_info = KD.get_anime_episode('%sAnime/%s/Episode-021?id=22589' %
                                       (desktop.BASE_URL, 'Nichijou'))
        self.assertGreater(len(ep_info), 0, "Invalid url")
        self.assertTrue('http' in ep_info, "Invalid URL")


if __name__ == '__main__':
    print 'Running test...'
    unittest.main()
