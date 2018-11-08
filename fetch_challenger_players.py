from get_all_challenger_data import get_match_history_data
import requests
import json
from tqdm import tqdm

API_URL = '.api.riotgames.com/lol/'
API_KEY = '?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
CHALLENGER_ENDPT = 'league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5'
ACCOUNT_ID = 'summoner/v3/summoners/'


def get_challenger_game_data(region):
    r = requests.get('https://'+region+API_URL +
                     CHALLENGER_ENDPT+API_KEY,)

    challengers = r.json()

    challenger_info = []

    for entry in tqdm(challengers['entries'][:2]):
        r = requests.get('https://' + region+API_URL +
                         ACCOUNT_ID + entry['playerOrTeamId'] + API_KEY)

        challenger_account_id = r.json()["accountId"]

        challenger_info.append(str(challenger_account_id))

    print('Challenger players being queried:', challenger_info)

    # # Lazy 'memoize'
    # with open('challengerlist.txt', 'w') as f:
    #     f.write(challenger_info)

    challenger_data = []

    for player_id in challenger_info:
        get_match_history_data(region, player_id)


if __name__ == '__main__':
    print(get_challenger_game_data('euw1'))
