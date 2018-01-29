## What Is EasyKissAnime?
EasyKissAnime is a quick and easy to use python api to get everything what you needed done with ease. It can retrieve all sorts of data such as air dates, summaries, video urls etc. To get started as fast as possible check out `example.py` to get started!

## Things to know
There's two base modules which could be used. One is a desktop module which uses the desktop website and the other is a mobile module which sticks to the mobile website(The mobile website module is currently being worked on). **Most** functions in the `KissAnime` object return a "meta object". A meta object is essentially all the information of the requested data in an easy to use form. Meta objects can return data in multiple ways, they call can be printed, they can be accessed like dictionaries, they all have variables, can return a dictionary of all the data and lastly they have specific functions to return the data as well.

## API Reference
* [Desktop](#desktop)
  * [KissAnime](#kissanime)
    * [get\_random\_anime](#get-random-anime)
    * [search](#search)
    * [get\_anime\_list](#get-anime-list)
    * [get\_anime\_info](#get-anime-info)
    * [get\_anime\_episode](#get-anime-episode)
  * [Meta Objects](#meta-objects)
    * [AnimeMetaObject](#animemetaobject)
    * [AnimeSearchObject](#animesearchobject)
    * [AnimeListObject](#animelistobject)
    * [AnimeEpisodeInfoObject](#animeepisodeinfoobject)
    * [AnimeEpisodeMetaObject](#animeepisodemetaobject)

# Desktop
The desktop module is mainly used for the desktop website. The module does however also make use of the mobile website. The reason for this is to bypass the "captcha" that is used when trying to view videos. As of right now this is the only way to get around the captcha.

## KissAnime
In order to use the API you need to first initialize it. This can easily be done with just calling
```kiss_desktop = desktop.KissAnime()```
Initalization will take about 10 seconds on the first startup. This is due to cloudflares automated captcha being stored. Once the captcha is solved it's stored in an sqlite3 database called `cloudflare.db`. Everytime you initalize `desktop.KissAnime()`, the sqlite3 database will be checked and the cookies will be validated. If they still work the bootup process will be a lot faster, however if the cookies have expired you would need to wait.

### Get Random Anime
`get_random_anime` takes two arguments which are both optional and are strings. This function also returns a [AnimeMetaObject](#animemetaobject). It can take a `genre` which can range from `All, Action, Adventure, Cars, Cartoon, Comedy, Dementia, Demons, Drama, Dub, Ecchi, Fantasy, Game, Harem, Historical, Horror, Josei, Kids, Magic, Martial-Arts, Mecha, Military, Movie, Music, Mystery, ONA, OVA, Parody, Police, Psychological, Romance, Samurai, School, Sci-Fi, Seinen, Shoujo, Shoujo-Ai, Shounen, Shounen-Ai, Slice-of-Life, Space, Special, Sports, Super-Power, Supernatural, Thriller, Vampire, Yuri`. This function also can take the name of multiple animes to be excluded from the random result. Each anime being excluded must have their spaces replaced with `-` and must end with `;`.

Example Usage:
```py
kiss_desktop = desktop.KissAnime()
random_anime = kiss_desktop.get_random_anime(genre='Action', excluded_anime='Yu-Gi-Oh-Arc-V-Dub;Black-Rock-Shooter-TV;')
print random_anime # Prints a random action anime which isn't Yu-Gi-Oh or black rock shooter

print kiss_desktop.get_random_anime() # Prints a completely random anime
```

### Search
`search` takes two optional arguments. The first argument is the search term/keyword which by default is an empty string. The second argument is a search type which by default is set to `Anime`. Internally the search used is the "Search Suggest" feature provided by KissAnime. The `search` function returns an array of [AnimeSearchObject's](#animesearchobject).

Example Usage:
```py
kiss_desktop = desktop.KissAnime()
results = kiss_desktop.search(keyword='Dragon Ball')
for result in results: # Loop search result array
    print result # Prints all search results

results2 = kiss_desktop.search('Naruto')
for result in results2: # Loop search result array
    print result # Prints all search results
```

### Get Anime List
`get_anime_list` takes two optional arguments. This function is to retrieve a list of animes starting with a specific letter. The `letter_filter` can be set from A->Z and the # character. By default the letter filter is set to an empty string which indicates that all animes should be listed. `letter_filter` is also not case sensitive so both upper and lowercase letters can be used. The second argument is the page number, by default the page is 0. The page can be changed by the `page` argument which by default is 0. The `get_anime_list` function returns an array of [AnimeListObject's](#animelistobject).

Example Usage:
```py
kiss_desktop = desktop.KissAnime()
anime_list = kiss_desktop.get_anime_list(letter_filter='A', page=2) # Get animes starting with A from page 2
for anime in anime_list: # Loop anime list array
    print anime # Print AnimeListObject

anime_list2 = kiss_desktop.get_anime_list(page=5) # Get all animes from page 5
for anime in anime_list2: # Loop anime list array
    print anime # Print AnimeListObject
```

### Get Anime Info
`get_anime_info` takes one argument. This argument can be one of multiple things. It either can be a [MetaObject](#meta-objects) which has the method `get_url` or it can take a string which is the URL of the anime page. This returns the most information about a specific anime. It contains episode information, descriptions, tags, names, amount of views etc. `get_anime_info` returns a [AnimeEpisodeMetaObject](#animeepisodemetaobject). 

Example Usage:
```py
kiss_desktop = desktop.KissAnime()
random_anime = kiss_desktop.get_random_anime() # Get a random anime
anime_info = kiss_desktop.get_anime_info(random_anime) # Get information about the random anime
print anime_info # print out all anime info
print kiss_desktop.get_anime_info('http://kissanime.ru/Anime/One-Piece') # Get information about one piece
```

### Get Anime Episode
`get_anime_episode` takes one argument. This argument can be one of multiple things. It either can be a [AnimeEpisodeInfoObject](#animeepisodeinfoobject) or a url to a specific episode. This returns a string of the video URL of the episode specified.

Example Usage:  
```py
kiss_desktop = desktop.KissAnime()
random_anime = kiss_desktop.get_random_anime() # Get a random anime
anime_info = kiss_desktop.get_anime_info(random_anime) # Get information 
print kiss_desktop.get_anime_episode(anime_info.get_episodes()[0])
```

## Meta Objects
All meta objects share simlar types of methods and follow the same general structure. All arguments for meta object creation are optional with the default value as an empty array or the string `N/A`. All meta objects also can be accessed like a dictionary `MetaObject['key']`. All meta objects can also be converted to a string and printed `print MetaObject`. All meta objects can have all their data returned as a dictionary as well `MetaObject.dictionary()`. Meta objects lastly have getters with the following format `MetaObject.get_*()` where `*` is the key you want. An example to use all these methods is as follows if the meta object has the key "title".

Example Usage:
```py
print MetaObject['title']
print MetaObject.dictionary()['title']
print MetaObject.get_title()
print MetaObject # Prints all keys and their values
```

### AnimeMetaObject

| Key         | Description                | Type             |
| :---------- | :------------------------: | ---------------: |
| title       | Anime title                | String           |
| url         | Url to the anime info page | String           |
| tags        | Anime tags/genres          | Array of strings |
| description | Anime description/summary  | String           |

### AnimeSearchObject

| Key    | Description                | Type   |
| :----- | :------------------------: | -----: |
| title  | Anime title                | String |
| url    | Url to the anime info page | String |

### AnimeListObject

| Key    | Description                  | Type   |
| :----- | :--------------------------: | -----: |
| title  | Anime title                  | String |
| url    | Url to the anime info page   | String |
| status | Airing status/Latest Episode | String |

### AnimeEpisodeInfoObject

| Key    | Description           | Type    |
| :----- | :-------------------: | ------: |
| title  | Episode title         | String  |
| url    | Url to the video page | String  |
| date   | Episode upload date   | String  |

### AnimeEpisodeMetaObject

| Key           | Description                                  | Type                            |
| :------------ | :------------------------------------------: | ------------------------------: |
| title         | Anime title                                  | String                          |
| other_names   | List of other titles the anime is refered as | Array of strings                |
| tags          | List of tags/genres                          | Array of strings                |
| air_date      | The next episode air date                    | String                          |
| status        | Current airing status                        | String                          |
| views         | Total amount of anime views                  | String                          |
| summary       | Description/Summary of the anime             | String                          |
| episodes      | Information about each episode               | Array of AnimeEpisodeMetaObject |
