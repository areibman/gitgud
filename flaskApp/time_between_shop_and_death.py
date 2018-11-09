import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import requests

from plotly import __version__
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import datetime
import scipy.stats as stats


def get_player_recall_history(player_id, champion_id, region):
    API_URL = '.api.riotgames.com/lol/'
    API_KEY = '?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
    MATCH_ID_ENDPOINT = 'match/v3/matchlists/by-account/'
    GAME_TIMELINE_ENDPOINT = 'match/v3/timelines/by-match/'
    MATCH_INFORMATION_ENDPOINT = 'match/v3/matches/'

    r = requests.get('https://'+region+API_URL +
                     MATCH_ID_ENDPOINT+str(player_id)+API_KEY)
    matches = r.json()

    match_list = [match['gameId']
                  for match in matches['matches'] if str(match['champion']) == str(champion_id)]

    match_timelines = {}
    for match in match_list:
        r = requests.get('https://'+region+API_URL +
                         GAME_TIMELINE_ENDPOINT+str(match)+API_KEY)
        match_timelines[match] = r.json()
        # Query the participant ID from a new request, and ad it to the match_timelines dict
        pid_request = requests.get(
            'https://'+region+API_URL+MATCH_INFORMATION_ENDPOINT+str(match)+API_KEY)
        pid_json = pid_request.json()

        # Find the participant ID and add it as a key to our megadict
        for participant in pid_json['participants']:
            if str(participant['championId']) == str(champion_id):
                match_timelines[match]['participantId'] = participant['participantId']
    return match_timelines

def get_player_time_between_death(match_timelines):
    """"""
    death_times = []
    for match in match_timelines:
        participantId = match_timelines[match]['participantId']
        #   Items purchased
        item_purchase_events = []
        print('match_timeline frames',len(match_timelines[match]['frames']))
        for frame in match_timelines[match]['frames']:
            for event in frame['events']:
                if event['type'] == 'ITEM_PURCHASED' and event['timestamp'] > 180000:
                    item_purchase_events.append(event)

        # Filter items purchased to only those made by the participant
        player_buys = []
        print('item_purchase_events*********************', len(item_purchase_events))
        for purchase in item_purchase_events:
            if str(purchase['participantId']) == str(participantId):
                player_buys.append(purchase)

        #   Champions Killed
        champion_kills = []
        for frame in match_timelines[match]['frames']:
            for event in frame['events']:
                if event['type'] == 'CHAMPION_KILL':
                    champion_kills.append(event)
#                   if purchase['participantId']!= participantId:
# #                     print(purchase['timestamp']['victimId'], participantId)
        time_betw_death_and_back = []
        for purchase in player_buys:
            for kill in champion_kills:
                if str(kill['victimId']) == str(participantId) and (kill['timestamp'] > purchase['timestamp']):
                    time_betw_death_and_back.append(
                        kill['timestamp']-purchase['timestamp'])
                    continue
                else:
                    pass

        if time_betw_death_and_back:
            death_times.append(time_betw_death_and_back)

    return [t[0] for t in death_times]


def get_challenger_time_between_death(champion):
    """
    """
    death_times = []

    for game_dump in os.listdir('./game_dumps'):
        df = pd.DataFrame()
        try:
            with open('./game_dumps/' + game_dump, 'r') as f:
                data = json.load(f)
            temp = pd.DataFrame(data['timeline']['frames'])
            participants = data['participants']

            champion_in_game = False
            for participant in participants:
                if str(participant['championId']) == str(champion):
                    champion_in_game = True
                    break
            participantId = participant['participantId']
            if not champion_in_game:
                continue

        except:
            continue

        df = df.append(temp)

    #   Items purchased
        item_purchase_events = []
        for index, row in df['events'].iteritems():
            for event in row:
                if event['type'] == "ITEM_PURCHASED" and event['timestamp'] > 180000:
                    item_purchase_events.append(event)

    #   Champions Killed
        champion_kills = []
        for index, row in df['events'].iteritems():
            for event in row:
                if event['type'] == "CHAMPION_KILL":
                    champion_kills.append(event)

        # Filter items purchased to only those made by the participant
        player_buys = []
        for purchase in item_purchase_events:
            if purchase['participantId'] == participantId:
                player_buys.append(purchase)

        time_betw_death_and_back = []
        for purchase in player_buys:
            for kill in champion_kills:
                if str(kill['victimId']) == str(participantId) and (kill['timestamp'] > purchase['timestamp']):
                    time_betw_death_and_back.append(
                        kill['timestamp']-purchase['timestamp'])
                    continue
                else:
                    pass

        if time_betw_death_and_back:
            death_times.append(time_betw_death_and_back)

    return [t[0] for t in death_times]


def save_shop_graph(champion_id, player_id, region):
    player_match_history = get_player_recall_history(
        player_id=player_id, champion_id=champion_id, region=region)
    player_time_between_death = get_player_time_between_death(
        player_match_history)
    challenger_time_between_purchase_and_death = get_challenger_time_between_death(
        champion_id)

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    fig = plt.figure(dpi=100)
    plt.rc('font', **font)
    plt.yticks([])
    plt.title('Time spent between item purchase and death')
    ax = sns.kdeplot([purchase/1000 for purchase in challenger_time_between_purchase_and_death], shade=True).set(xlim=(0, 1800))
    ax2 = sns.kdeplot([purchase/1000 for purchase in player_time_between_death], shade=True).set(xlim=(0, 1800))

    plt.xlabel('In-game seconds')

    plt.legend(('Challengers',
                'You'))

    plt.savefig("Time-between-deaths.svg", transparent=True)
    os.rename('Time-between-deaths.svg', 'svg_deaths.txt')
    with open('svg_deaths.txt', 'r') as f:
        svg = f.read()
    plt.close()

    return {'key':'Shop n\' Drop' ,'svgs':[svg]}
