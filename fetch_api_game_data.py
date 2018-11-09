import requests
import time
from tqdm import tqdm
import json

API_URL = '.api.riotgames.com/lol/'
API_KEY = '?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
MATCH_ID_ENDPOINT = 'match/v3/matchlists/by-account/'
MATCH_INFORMATION_ENDPOINT = 'match/v3/matches/'
GAME_TIMELINE_ENDPOINT = 'match/v3/timelines/by-match/'


def get_match_history_data(region, player_id, champion="-1"):
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

        particpant_id = ''
        champion_id = ''

        for participant in match_info['participantIdentities']:
            if str(participant['player']['accountId']) == player_id:
                particpant_id = participant['participantId']
                break

        for participant in match_info['participants']:
            if participant['participantId'] == particpant_id:
                champion_id = participant['championId']
                break

        match_info_list.append({
            'match_id': match_info['gameId'],
            'champion_id': champion_id,
            'participant_id': particpant_id
        })

        time.sleep(0.2)

    if champion_id != "-1":
        subset_matches = [
            match for match in match_info_list if match['champion_id'] == champion]
    else:
        subset_matches = match_info_list

    # ## Step 3:
    # Get participant ID from step 2 and collect data

    player_match_timeline = {}

    for match in tqdm(subset_matches):
        game_timeline_request =\
            requests.get('https://'+region+API_URL + GAME_TIMELINE_ENDPOINT +
                         str(match['match_id'])+API_KEY)

        game_timeline = game_timeline_request.json()

        player_frames_list = []

        for frame in game_timeline['frames']:
            player_frames_list.append(
                frame['participantFrames'][str(match['participant_id'])])

        player_match_timeline[match['match_id']] = player_frames_list

        time.sleep(0.01)

    return player_match_timeline


if __name__ == '__main__':
    print(get_match_history_data('euw1', '219693852', '85'))
