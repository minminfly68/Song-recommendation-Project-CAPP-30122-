'''
Crawling the lyrics on Genius Website, then generate the lyrics
dictionary, and finally write into json file.
Chun Hu, Yimin Li, Tianyue Niu
'''

import json
import os
import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def crawl(filename='top10s.csv'):
    '''
    Crawl the lyrics based on the most popular csv file and export
    it to a json file

    Input:
        filename: (string) the top songs databse (default: 10.csv)
    '''
    cwd = os.path.dirname(__file__)
    top_10s_path = os.path.join(cwd, filename)
    df = pd.read_csv(top_10s_path)
    ls_titles = df['title'].tolist()
    ls_artists = df['artist'].tolist()

    dict_lyric, lyrics_found, lyrics_not_found = scrape_lyrics(ls_artists,
                                                               ls_titles,
                                                               False)

    df_not_found = df.loc[df['title'].isin(lyrics_not_found)]

    ls_artists_not_found = df_not_found['artist'].tolist()
    ls_titles_not_found = df_not_found['title'].tolist()

    # Web scraping for the second time for those not-found songs
    # Change the url generation model by applying some regular expressions
    dict_new, lyrics_new, lyrics_not_new = scrape_lyrics(ls_artists_not_found,
                                                         ls_titles_not_found,
                                                         True)
    lyrics_found_final = lyrics_found + lyrics_new
    dict_lyric.update(dict_new)

    with open('lyrics_file.json', 'w') as file:
        json.dump(dict_lyric, file)

def scrape_lyrics(ls_artists, ls_titles, revised_title):
    '''
    Scrape lyrics for one time given the list of artists and titles
    Inputs:
        ls_artists: (list of strings) list of artists' name
        ls_titles: (list of strings) list of songs' titles
        revised_title: (bool) Determine whether it is the first or second
                      crawl to determine whether to call construct_title
    '''
    delay = 0.1
    lyrics_found = []
    lyrics_not_found = []
    dict_lyric = {}
    for i in range(len(ls_artists)):
        if revised_title:
            ls_titles[i] = construct_title(ls_titles[i])
        final_url = construct_final_url(ls_artists[i], ls_titles[i])
        try:
            request = requests.get(final_url)
            soup = BeautifulSoup(request.text, 'html.parser')
            lyrics = soup.find("div", class_="lyrics").get_text()
            dict_lyric[ls_titles[i]] = lyrics
            print("Lyrics successfully scraped for:" + ls_titles[i])
            lyrics_found.append(ls_titles[i])

        except:
            lyrics_not_found.append(ls_titles[i])

        finally:
            time.sleep(delay)
    return dict_lyric, lyrics_found, lyrics_not_found

def construct_final_url(artist, title):
    '''
    Generate a final url based on title and artist
    Inputs:
        artist: (string) artist of the song
        title: (string) title of the song
    Output:
        final_url: (string) url to crawl
    '''
    base_url = "https://genius.com/{}-{}-lyrics"

    title = re.sub(r'\W+', ' ', title)
    artist = re.sub(r'\W+', ' ', artist)
    title = title.lower()
    title = title.replace(" ", "-")
    artist = artist.replace(" ", "-")

    final_url = base_url.format(artist, title)
    return final_url

def construct_title(s):
    '''
    Reconstruct the tile for the second crawl by using regular expression
    Input:
        s: (string) title that cannot be found in the first crawl
    Output:
        s: (string) reconstructed title after using the regular expression
    '''
    pattern = r'\(.*?\)'
    s = re.sub(pattern, '', s)
    s = s.split('-', maxsplit=1)[0]
    s = re.sub(r'\s+$', '', s)
    s = s.replace("'", "")
    return s


if __name__ == "__main__":
    crawl()
