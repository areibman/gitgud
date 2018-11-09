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


def get_challenger_gold_delta(champion):
    """
    """
    gold_count_dict = {}

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

    #   log gold at timestamp
        current_gold_list = []
        total_gold_list = []
        for index, row in df['participantFrames'].iteritems():
            current_gold_list.append(row[str(participantId)]['currentGold'])
            total_gold_list.append(row[str(participantId)]['totalGold'])

        gold_count_dict[game_dump] = {
            'current_gold': current_gold_list, 'total_gold': total_gold_list}

    recordings_remaining = True
    num_matches = len(gold_count_dict.keys())
    currents = []
    index = 0
    while recordings_remaining:
        currents_sum = 0
        for match in gold_count_dict:
            if index < len(gold_count_dict[match]['current_gold']):
                currents_sum += gold_count_dict[match]['current_gold'][index]
            else:
                num_matches -= 1
        if num_matches <= 0:
            break

        currents.append(currents_sum/num_matches)
        num_matches = len(gold_count_dict.keys())
        index += 1

    totals = []
    index = 0
    num_matches = len(gold_count_dict.keys())
    while recordings_remaining:
        totals_sum = 0
        for match in gold_count_dict:
            if index < len(gold_count_dict[match]['total_gold']):
                totals_sum += gold_count_dict[match]['total_gold'][index]
            else:
                num_matches -= 1
        if num_matches <= 0:
            break

        totals.append(totals_sum/num_matches)
        num_matches = len(gold_count_dict.keys())
        index += 1

    return currents, totals


def get_player_gold_delta(match_timelines):
    """
    """
    gold_count_dict = {}

    for match in match_timelines:
        participantId = match_timelines[match]['participantId']
        #   Items purchased
        current_gold = []
        total_gold = []

        for frame in match_timelines[match]['frames']:

            current_gold.append(
                frame['participantFrames'][str(participantId)]['currentGold'])
            total_gold.append(frame['participantFrames']
                              [str(participantId)]['totalGold'])

        gold_count_dict[match] = {
            'current_gold': current_gold, 'total_gold': total_gold}

    recordings_remaining = True
    num_matches = len(gold_count_dict.keys())
    currents = []
    index = 0
    while recordings_remaining:
        currents_sum = 0
        for match in gold_count_dict:
            if index < len(gold_count_dict[match]['current_gold']):
                currents_sum += gold_count_dict[match]['current_gold'][index]
            else:
                num_matches -= 1
        if num_matches <= 0:
            break

        currents.append(currents_sum/num_matches)
        num_matches = len(gold_count_dict.keys())
        index += 1

    totals = []
    index = 0
    num_matches = len(gold_count_dict.keys())
    while recordings_remaining:
        totals_sum = 0
        for match in gold_count_dict:
            if index < len(gold_count_dict[match]['total_gold']):
                totals_sum += gold_count_dict[match]['total_gold'][index]
            else:
                num_matches -= 1
        if num_matches <= 0:
            break

        totals.append(totals_sum/num_matches)
        num_matches = len(gold_count_dict.keys())
        index += 1

    return currents, totals


def get_player_recall_history(player_id, champion_id, region):
    API_URL = '.api.riotgames.com/lol/'
    API_KEY = '?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
    MATCH_ID_ENDPOINT = 'match/v3/matchlists/by-account/'
    GAME_TIMELINE_ENDPOINT = 'match/v3/timelines/by-match/'
    MATCH_INFORMATION_ENDPOINT = 'match/v3/matches/'
    player_id = str(player_id)
    r = requests.get('https://'+region+API_URL +
                     MATCH_ID_ENDPOINT+player_id+API_KEY)
    matches = r.json()
    print('https://'+region+API_URL +
          MATCH_ID_ENDPOINT+player_id+API_KEY)
    match_list = []
    for match in matches['matches']:
        if str(match['champion']) == str(champion_id):
            match_list.append(match['gameId'])

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


def save_gold_graph(champion_id, player_id, region):
    player_match_history = get_player_recall_history(
        player_id, champion_id, region)
    player_gold_delta = get_player_gold_delta(player_match_history)

    challenger_gold_delta = get_challenger_gold_delta(champion_id)
    plt.figure(dpi=150)
    sns.set(style="whitegrid")
    sns.boxplot(data=[player_gold_delta[0], challenger_gold_delta[0]])
    plt.title('Current gold held unused (sampled every min)')
    plt.ylabel('Gold count held')
    plt.xlabel(
        '   Player gold held unused            Challengers gold held unused')
    plt.savefig("Gold-saved.svg", transparent=True)
    os.rename('Gold-saved.svg', 'svg_gold.txt')
    with open('svg_gold.txt', 'r') as f:
        svg = f.read()

    plt.close()

    return {'key': 'Gold held unused', 'svgs': [svg]}


def save_gold_timeline(champion_id, player_id, region):
    player_match_history = get_player_recall_history(
        player_id, champion_id, region)
    player_gold_delta = get_player_gold_delta(player_match_history)

    challenger_gold_delta = get_challenger_gold_delta(champion_id)
    plt.figure(dpi=150)
    fig = plt.figure(dpi=100)

    plt.ylabel('Gold count')
    plt.xlabel('In-game minutes')

    plt.plot(np.array(golds[0]))
    plt.plot(np.array(player_gold_delta[0]))

    plt.savefig("Gold-over-time.svg", transparent=True)
    os.rename("Gold-over-time.svg", 'svg_gold_graph.txt')
    with open('svg_gold_graph.txt', 'r') as f:
        svg = f.read()

    plt.close()

    return {'key': 'Gold held over time', 'svgs': [svg]}
