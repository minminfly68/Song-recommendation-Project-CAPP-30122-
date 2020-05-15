'''
Query Result
Chun Hu, Yimin Li, Tianyue Niu
'''

import pandas as pd
import random
import os

cwd = os.path.dirname(__file__)
top_song_path = os.path.join(cwd, 'top_songs.csv')


def execute(dict_command):
    '''
    Input: dict_command(dict), a dictionary of user's input
           e.g. dict_command might look something like this:
           {'happy': 'neutral', 'relaxing': 'relaxing', 'yes': 'no'}
    Output: a song's title randomly selected from a selected list (str)
    '''
    df = pd.read_csv(top_song_path).drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
    df = df.dropna(axis=0)

    dict_sentiment = {'sad': 'sentiment < 0',
                      'neutral': '0 <= sentiment <= 0.2',
                      'happy': 'sentiment > 0.2'}
    dict_energy = {'relaxing': 'nrgy < 40',
                   'neutral': '40<= nrgy <= 60',
                   'intensive': 'nrgy > 60'}
    dict_year = {'yes': 'year >= 2018', 'no': 'year < 2018'}
    ls_dict = [dict_sentiment, dict_energy, dict_year]

    if not dict_command:
        return "Oops! You haven't told us your preferences :)"

    str_command = ''

    for key_, value_ in dict_command.items():
        for dict_ in ls_dict:
            if key_ in dict_:
                str_command += dict_[value_] + ' and '
    str_command = str_command[:-5]
    ls_title = list(df.query(str_command)['title'])

    return random.choice(ls_title)
