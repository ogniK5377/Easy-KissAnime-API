"""Desktop related KissAnime usage."""
import sqlite3
import urllib
import urlparse
import cfscrape
import requests
import lxml.html
from lxml.cssselect import CSSSelector

BASE_URL = "http://kissanime.ru/"

MOBILE_BASE_URL = 'http://kissanime.ru/Mobile/'

USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 \
Firefox/56.0"

# Mobile user agent is required to get around the captcha

MOBILE_USERAGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) \
AppleWebKit/604.1.38 (KHTML, like Gecko) \
Version/11.0 Mobile/15A402 Safari/604.1"


class ConnectionHandler(object):
    """Kissanime Desktop handler"""
    def __init__(self, database='cloudflare.db'):
        self.is_initalized = False
        self.cf_db = sqlite3.connect(database)  # Create/Load DB on disk
        if not self.initalize_sqldb():  # Initalize if not already created
         raise Exception("cannot initalize sql db")
        self.scrape = self.setup_cloudflare()  # Main setup here
        self.mobile_scrape = self.setup_mobilecloudflare()  # Captcha bypass
        self.is_initalized = True

    def __del__(self):
        """Free up any objects which need to be closed"""
        self.is_initalized = False  # Not needed but support can be added
        if self.cf_db:  # Close db on cleanup
            self.cf_db.close()

    def initalize_sqldb(self):
        """Initalize the SQL database if it's not already setup. Also validate
        that the sql database
        actually created and is valid."""
        if self.cf_db is None:  # DB Invalid
            return False
        self.cursor = self.cf_db.cursor()  # Needed to execute queries
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Cookies
        (DomainID INTEGER PRIMARY KEY UNIQUE, Cookies TEXT NOT NULL, UserAgent\
         TEXT NOT NULL);''')
        self.cf_db.commit()  # Commit changes to the DB
        return True

    def setup_mobilecloudflare(self):
        """Setup mobile cloudflare to bypass captcha do get video links"""
        return self.setup_cloudflare(domain_id=1, user_agent=MOBILE_USERAGENT)

    def setup_cloudflare(self, domain_id=0, user_agent=USERAGENT):
        """Check if new cookies are needed or retrieve existing cookies"""
        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})
        self.cursor.execute('''SELECT * FROM Cookies
        WHERE DomainID=''' + str(domain_id))  # DomainID 0=Desktop, 1=Mobile
        sql_row = self.cursor.fetchone()
        if sql_row is None:  # There actually isn't any cookies to check
            scrape = cfscrape.create_scraper(sess=session)
            tkn, agt = scrape.get_cookie_string(
                BASE_URL, user_agent=user_agent
            )
            self.cursor.execute('''INSERT INTO Cookies(DomainID, Cookies, UserAgent)
            VALUES(?, ?, ?);''', (domain_id, tkn, agt))
            self.cf_db.commit()
            return scrape
        else:
            session.headers.update({
                'Cookie': sql_row[1],
            })
            req = session.get(BASE_URL)
            if req.status_code == 200:  # Valid cookie still
                return cfscrape.create_scraper(sess=session)
            else:  # Cookie needs to be updated
                session.headers.update({
                    'Cookie': '',
                })  # Clear previous cookie
                scrape = cfscrape.create_scraper(sess=session)
                tkn, agt = scrape.get_cookie_string(
                    BASE_URL, user_agent=user_agent
                )
                self.cursor.execute('''UPDATE Cookies
                SET Cookies=?, UserAgent=? WHERE DomainID=?''', (
                    tkn, agt, domain_id
                ))
                session.headers.update({
                    'Cookie': tkn
                })
                return scrape


class AnimeMetaObject(object):
    """Basic anime information meta object"""
    def __init__(self, title='N/A', url='N/A', tags='N/A', description='N/A'):

        self.title = title.encode('utf-8')
        self.url = url.encode('utf-8')
        self.tags = [tag.encode('utf-8') for tag in tags]
        self.description = description.encode('utf-8')
        
        self.dictionary = {
                           'title':self.title,
                            'url':self.url,
                            'tags':self.tags,
                            'description':self.description
            
                          }
        
    def __getitem__(self, key):
        return self.dictionary[key.lower()]

    def __str__(self):
        cur_str = 'Title:       %s\n' % self.title
        cur_str += 'Tags:        %s\n' % ', '.join(self.tags)
        cur_str += 'URL:         %s\n' % self.url
        cur_str += 'Description: %s' % self.description
        return cur_str


class AnimeSearchObject(object):
    """Anime meta data for search results"""
    def __init__(self, title='N/A', url='N/A'):

        self.title = title.encode('utf-8')
        self.url = url.encode('utf-8')
        self.dictionary = {
                            'title':self.title,
                            'url':self.url
                          }
        
    def __getitem__(self, key):
        return self.dictionary[key.lower()]

    def __str__(self):
        cur_str = 'Title:       %s\n' % self.title
        cur_str += 'URL:         %s' % self.url
        return cur_str


class AnimeListObject(object):
    """Anime meta data for the anime list"""
    def __init__(self, title='N/A', url='N/A', status='N/A'):

        self.title = title.encode('utf-8')
        self.url = url.encode('utf-8')
        self.status = status.encode('utf-8')
        self.dictionary = {
            'title': self.title,
            'url': self.url,
            'status': self.status
        }

    def __getitem__(self, key):
        return self.dictionary[key.lower()]

    def __str__(self):
        cur_str = 'Title:       %s\n' % self.title
        cur_str += 'Status:      %s\n' % self.status
        cur_str += 'URL:         %s' % self.url
        return cur_str


class AnimeEpisodeInfoObject(object):
    """Anime meta data for the anime episodes"""
    def __init__(self, title='N/A', url='N/A', date='N/A'):
        title = title or 'N/A'
        url = url or 'N/A'
        date = date or 'N/A'

        self.title = title.encode('utf-8')
        self.url = url.encode('utf-8')
        self.date = date.encode('utf-8')
        self.dictionary = {
            'title': self.title,
            'url': self.url,
            'date': self.date
        }

    def __getitem__(self, key):
        return self.dictionary[key.lower()]

    def __str__(self):
        cur_str = 'Title:       %s\n' % self.title
        cur_str += 'Date:        %s\n' % self.date
        cur_str += 'URL:         %s' % self.url
        return cur_str


class AnimeEpisodeMetaObject(object):
    """Anime meta data"""
    def __init__(self, title='N/A', other_names=None, tags=None,
                 air_date='N/A', status='N/A', views='N/A',
                 summary='N/A', episodes=None):
       
        self.title = title.encode('utf-8')
        self.other_names = other_names
        self.tags = tags
        self.air_date = air_date.encode('utf-8')
        self.status = status.encode('utf-8')
        self.views = views.encode('utf-8')
        self.summary = summary.encode('utf-8')
        self.episodes = episodes
        self.dictionary = {
                           'title':self.title,
                            'other_names': self.other_names,
                            'tags': self.tags,
                            'air_date':self.air_date,
                            'status': self.status,
                            'views':self.view,
                            'summary':self.summary,
                            'episodes':self.episodes,
                           }
                         

    def __getitem__(self, key):
        return self.dictionary[key.lower()]

    def __str__(self):
        cur_str = 'Title:        %s\n' % self.title
        cur_str += 'Other Titles: %s\n' % ", ".join(self.other_names)
        cur_str += 'Tags:         %s\n' % ", ".join(self.tags)
        cur_str += 'AirDate:      %s\n' % self.air_date
        cur_str += 'Status:       %s\n' % self.status
        cur_str += 'Views:        %s\n' % self.views
        cur_str += 'Summary:      %s\n' % self.summary
        cur_str += 'Episodes:       \n'
        for episode in self.episodes:
            cur_str += '          %s\n' % episode.get_title()
        cur_str = cur_str[:-1]
        return cur_str


class KissAnime(object):
    """Main API Object"""
    def __init__(self):
        self.conn = ConnectionHandler()  # Initalize connection handler
        assert self.conn.is_initalized

    def get_random_anime(self, genre='All', excluded_anime=''):
        """Returns an AnimeMetaObject for a random anime"""
        params = urllib.urlencode({
            'selectGenre': genre,
            'excludedAnime': excluded_anime
        })
        content = self.conn.scrape.post('%sGetRandomAnime?%s' % (
            BASE_URL, params
        ))
        tree = lxml.html.fromstring(content.text)
        paragraphs = CSSSelector('p')(tree)
        if paragraphs is None or len(paragraphs) < 2:
            return None
        bigchar = CSSSelector('.bigChar')(tree)  # Holds title and URL
        if bigchar is None or len(bigchar) < 1:
            return None
        bigchar = bigchar[0]
        description = paragraphs[1].get('title')
        tags = [tag.text for tag in paragraphs[0].cssselect('a')]  # Tags a's
        title = bigchar.text
        url = BASE_URL[:-1] + bigchar.get('href')
        return AnimeMetaObject(title, url, tags, description)

    def search(self, keyword='', search_type='Anime'):
        """Returns an AnimeSearchObject for a specific search term"""
        content = self.conn.scrape.post('%sSearch/SearchSuggestx' % BASE_URL, {
            'type': search_type,
            'keyword': keyword
        })
        tree = lxml.html.fromstring(content.text)
        animes = CSSSelector('a')(tree)  # Everything is just a link
        animes = animes or []
        results = []
        for anime in animes:
            title = "".join([x for x in anime.itertext()])  # <span> iterator
            url = anime.get('href')  # All wrapped in <a>
            results.append(AnimeSearchObject(title, url))
        return results

    def get_anime_list(self, letter_filter='', page=0):
        """Returns an AnimeListObject and the max page count with a
        specific filter on a specific page if specified"""
        if letter_filter == '#':  # KissAnime refers to # as 0
            letter_filter = '0'
        params = urllib.urlencode({'c': letter_filter, 'page': page})
        content = self.conn.scrape.get('%sAnimeList?%s' % (BASE_URL, params))
        tree = lxml.html.fromstring(content.text)
        listing = CSSSelector('.listing tr')(tree)  # Get results
        if len(listing) < 3:
            return []
        results = []
        for i in range(2, len(listing)):  # First two results are garbage
            anime_listing = listing[i]
            title = "".join(
                [x.strip() for x in anime_listing[0].itertext()]  # Ignore tags
            )
            latest_episode = "".join(
                [x.strip() for x in anime_listing[1].itertext()]  # Ignore tags
            )
            url = BASE_URL[:-1]
            url += anime_listing[0].cssselect('a')[0].get('href')  # anime page
            results.append(AnimeListObject(title, url, latest_episode))
        return results

    def get_anime_info(self, obj):
        """Returns an AnimeInfoObject. A url,
        or any meta object can be passed"""
        url = ''
        if isinstance(obj, basestring):
            if obj[:1] == '/':
                url = BASE_URL[:-1] + obj
            else:
                url = obj  # Can take absolute url
        else:
            url = obj.get_url()  # Any anime meta object
        content = self.conn.scrape.get(url)
        tree = lxml.html.fromstring(content.text)
        listing = CSSSelector('.bigBarContainer')(tree)
        if listing is None or len(listing) < 2:
            return None
        pgraphs = listing[0].cssselect('p')
        if pgraphs is None or len(pgraphs) < 5:
            return None
        extra_info = []
        if len(pgraphs) == 6:  # some animes dont have an air date
            extra_info = [x.strip() for x in pgraphs[3].itertext()]
        else:
            extra_info = [x.strip() for x in pgraphs[2].itertext()]
        if len(extra_info) < 5:  # Not valid at all?
            return None
        title = listing[0].cssselect('.bigChar')[0]
        if title is None:
            title = 'N/A'
        else:
            title = title.text
        alt_names = [
            x.text.strip().encode('utf-8') for x in pgraphs[0].cssselect('a')
        ]
        tags = [
            x.text.strip().encode('utf-8') for x in pgraphs[1].cssselect('a')
        ]
        airdate = 'N/A'
        if len(pgraphs) == 6:  # Only if we have 6 <p>'s, airdate is present
            airdate = "".join([x.strip() for x in pgraphs[2].itertext()])[11:]
        status = extra_info[2]
        views = extra_info[4]
        summary = 'N/A'
        if len(pgraphs) == 6:  # Due to airdate, summary can be shifted
            summary = "".join([x.strip() for x in pgraphs[5].itertext()])
        else:
            summary = "".join([x.strip() for x in pgraphs[4].itertext()])

        ep_list = listing[1].cssselect('tr')
        ep_meta = []
        if len(ep_list) > 2:
            for i in range(2, len(ep_list)):  # First two are junk
                episode = ep_list[i]
                info = episode.cssselect('td')
                if len(info) < 2:
                    continue
                ep_name = "".join([x.strip() for x in info[0].itertext()])
                ep_url = BASE_URL[:-1]
                ep_url += info[0].cssselect('a')[0].get('href')
                ep_rel = info[1].text.strip()  # Remove whitespace
                ep_meta.append(AnimeEpisodeInfoObject(ep_name, ep_url, ep_rel))
        return AnimeEpisodeMetaObject(title, alt_names, tags,
                                      airdate, status, views, summary, ep_meta)

    def get_anime_episode(self, obj):
        """Returns video url"""
        url = ''
        if isinstance(obj, basestring):
            if obj[:1] == '/':
                url = BASE_URL[:-1] + obj
            else:
                url = obj  # Can take absolute url
        else:
            url = obj.get_url()  # Any anime meta object
        p_url = urlparse.urlparse(url)
        episode_id = urlparse.parse_qs(p_url.query)['id'][0]  # episode ID
        referer = BASE_URL + 'M' + p_url.path[:p_url.path.rfind('/')]  # EpName
        content = self.conn.mobile_scrape.post(
            '%sGetEpisode' % MOBILE_BASE_URL, {
                'eID': episode_id
            }, headers={
                'Referer': referer  # Needed or the request fails
            })  # Mobile site required to bypass captcha
        return content.text.split('|||')[0]  # Get video url
