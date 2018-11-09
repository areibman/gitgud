import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import requests
import time

import datetime
import scipy.stats as stats


def get_recalls_by_champion(champion):
    """
    """
    all_purchases = []

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

        recall_buys = []
    #   Remove items purchased after deaths
        for purchase in item_purchase_events:
            purchased_after_kill = False

            for kill in champion_kills:
                if purchase['timestamp'] < 30000 + kill['timestamp'] and purchase['timestamp'] > kill['timestamp'] - 30000:
                    if str(kill['victimId']) == str(purchase['participantId']):
                        purchased_after_kill = True
                        break
            if purchased_after_kill:
                continue
            else:
                recall_buys.append(purchase)

    #   Subest of all first buys
        players_with_first_buys = set()
        first_purchases = []
#         print(recall_buys)
#         for purchase in recall_buys:
#             if purchase['participantId'] in players_with_first_buys:
#                 continue
#             else:
#                 players_with_first_buys.add(purchase['participantId'])
#                 first_purchases.append(purchase)
        first_purchases.append(recall_buys[0])

#         if len(first_purchases) <10:
#             continue
        purchase_times = [time['timestamp']
                          for time in first_purchases if time['timestamp'] < 600000]
        all_purchases.extend(purchase_times)
    return all_purchases


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
    match_list= []
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


def get_recall_timestamps_for_player(match_timelines):
    print('matchTimelines',len(match_timelines))
    for match in match_timelines:
        participantId = match_timelines[match]['participantId']
        #   Items purchased
        item_purchase_events = []
        for frame in match_timelines[match]['frames']:

            for event in frame['events']:

                if event['type'] == 'ITEM_PURCHASED' and event['timestamp'] > 180000:
                    item_purchase_events.append(event)

        # Filter items purchased to only those made by the participant
        player_buys = []
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

        #  Ignore purchases after death
        recall_buys = []
        purchased_after_kill = False
        for purchase in player_buys:
            for kill in champion_kills:
                if str(kill['victimId']) == str(participantId):
                    if purchase['timestamp'] < 30000 + kill['timestamp'] and purchase['timestamp'] > kill['timestamp'] - 30000:
                        purchased_after_kill = True
                        break
            if purchased_after_kill:
                continue
            else:
                recall_buys.append(purchase)
    return [buy['timestamp'] for buy in recall_buys]

# ENDPOINT GO HERE!!!!


def save_fb_graph(champion_id, player_id, region_id):

    challenger_recall_times = get_recalls_by_champion(champion_id)
    player_data = get_player_recall_history(
        player_id=player_id, champion_id=champion_id, region=region_id)
    player_recall_times = get_recall_timestamps_for_player(player_data)
    print('YEET', len(challenger_recall_times), challenger_recall_times, len(player_recall_times), player_recall_times)
    if len(challenger_recall_times) == 0 or len(player_recall_times) == 0:
        return json.dumps([{'key':'First Recall Time' ,'svgs':['<span />']}])
    else:
        plt.figure(dpi=100)
        plt.yticks([])
        plt.title('First recall purchase times for Challenger Players (in seconds)')

        ax = sns.kdeplot(
            [purchase/1000 for purchase in challenger_recall_times], color='blue', shade=True)
        ax2 = sns.kdeplot(
            [purchase/1000 for purchase in player_recall_times], color='red', shade=True)

        plt.legend(('Challenger Player Average Recall','Your Average Recall'))
        plt.savefig("First-recall-purchase-for-player-single-match.svg", transparent=True)

        plt.close()
        os.rename('First-recall-purchase-for-player-single-match.svg', 'svg.txt')
        print('hey it saved!')
        with open('svg.txt', 'r') as f:
            svg = f.read()
        return {'key':'First Recall Time' ,'svgs':[svg]}
