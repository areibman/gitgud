
# coding: utf-8

# In[151]:


import requests
import time
from tqdm import tqdm
import json


# In[230]:


API_URL = R'''https://euw1.api.riotgames.com/lol/'''
API_KEY= R'?api_key=RGAPI-3a4ed2fd-dc8d-4bcc-acd5-360c10f25360'
MATCH_ID_ENDPOINT = R'match/v3/matchlists/by-account/'


MATCH_INFORMATION_ENDPOINT = 'match/v3/matches/'
PLAYER_ID = '219693852' # Change this later
CHAMPION_ID = 85 # Change this later


GAME_TIMELINE_ENDPOINT = r'match/v3/timelines/by-match/'


# ## Step 1 
# Get the matches

# In[153]:


r = requests.get(API_URL+MATCH_ID_ENDPOINT+PLAYER_ID+API_KEY,)


# In[154]:


matches = r.json()


# In[155]:


match_list = []

for match in matches['matches']:
    match_list.append(match['gameId'])


# ## Step 2 
# Get the game information

# In[225]:


match_info_list = []

for match in tqdm(match_list):
    match_info_request = requests.get(API_URL+MATCH_INFORMATION_ENDPOINT+str(match)+API_KEY,)
    match_info = match_info_request.json()
    
    
    particpant_id = ''
    champion_id = ''

    for participant in match_info['participantIdentities']:
        if str(participant['player']['accountId']) == PLAYER_ID:
            particpant_id = participant['participantId']
            break
    
    for participant in match_info['participants']:
        if participant['participantId'] == particpant_id:
            champion_id = participant['championId']
            break

    
    
    match_info_list.append({
                            'match_id': match_info['gameId'],
                            'champion_id':champion_id,
                            'participant_id': particpant_id
                           })
            
    time.sleep(0.2)


# In[231]:


subset_matches = [match for match in match_info_list if match['champion_id'] == CHAMPION_ID]


# ## Step 3:
# Get participant ID from step 2 and collect data

# In[236]:


player_match_timeline = {}

for match in tqdm(subset_matches):

    game_timeline_request = requests.get(API_URL+GAME_TIMELINE_ENDPOINT+str(match['match_id'])+API_KEY,)
    game_timeline = game_timeline_request.json()

    player_frames_list = []

    for frame in game_timeline['frames']:
        player_frames_list.append(frame['participantFrames'][str(match['participant_id'])])
        
    
    player_match_timeline[match['match_id']] = player_frames_list
    
    time.sleep(0.01)

