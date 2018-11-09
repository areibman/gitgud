import requests
import time
from tqdm import tqdm
import json

API_URL = '.api.riotgames.com/lol/'
API_KEY = '?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
MATCH_ID_ENDPOINT = 'match/v3/matchlists/by-account/'
MATCH_INFORMATION_ENDPOINT = 'match/v3/matches/'
GAME_TIMELINE_ENDPOINT = 'match/v3/timelines/by-match/'


def get_match_history_data(region, player_id):
    """
    Fetches game data given their unique player id
        can additionally filter data by champion
        args:
            Region: string that identifies region
            Player_id: string that uniquely identifies player
            Champion_id: string that identifies champion (optional)
        returns:
            json object containing timestamp and game data of player given the above parameters 
    """

    # ## Step 1
    # Get the matches

    r = requests.get('https://'+region+API_URL +
                     MATCH_ID_ENDPOINT+player_id+API_KEY)

    print("Current endpoint query:", 'https://'+region+API_URL +
          MATCH_ID_ENDPOINT+player_id+API_KEY)
    matches = r.json()

    match_list = []

    # Match id list
    for match in matches['matches']:
        match_list.append(match['gameId'])

    # ## Step 2
    # Get the game information

    match_info_list = []

    for match in tqdm(match_list):
        match_info_request =\
            requests.get('https://'+region+API_URL +
                         MATCH_INFORMATION_ENDPOINT+str(match)+API_KEY)

        match_info = match_info_request.json()

        game_timeline_request =\
            requests.get('https://'+region+API_URL + GAME_TIMELINE_ENDPOINT +
                         str(match)+API_KEY)

        game_timeline = game_timeline_request.json()

        match_info['timeline'] = game_timeline

    with open(f'./game_dumps/{match}.json', 'w') as f:
        f.write(json.dumps(match_info))

    return match_info
