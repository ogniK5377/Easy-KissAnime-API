"""EasyKissAnime API Example"""
from KissAnime import desktop

def main():
    """Entry point"""
    kiss_desktop = desktop.KissAnime()
    anime_search = kiss_desktop.search('Dragonball') # Returns array of search results
    print 'Dragonball Search Results'
    for search_result in anime_search:
        print search_result # Print all search info for every result
        print '-'*8
    anime_info = kiss_desktop.get_anime_info(anime_search[0])
    print 'Anime info for "%s"'%anime_search[0].get_title()
    print anime_info
    print '-'*16
    episode_url = kiss_desktop.get_anime_episode(anime_info.get_episodes()[0]) # Latest episode
    print 'Latest episode URL'
    print episode_url

if __name__ == '__main__':
    main()
