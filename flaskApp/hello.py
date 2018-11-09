from flask import Flask
from flask_cors import CORS
import json
import os
from pprint import pprint
from flask import request
from fetch_api_game_data import get_summoner_infos

app = Flask(__name__)
CORS(app)

@app.route('/teemo')
def hello_world():
    json_array = []
    trash_array = []
    for item in os.listdir('game_dumps/'):
        with open('game_dumps/' + item, 'r') as data_file:
            data = json.load(data_file)
        if data['gameDuration'] > 1200:
            json_array.append(data)
        else:
            os.remove('game_dumps/'+str(data['gameId'])+'.json')
            print('removed-'+str(data['gameId'])+'.json')

    return json.dumps(json_array)

@app.route('/summoner-data')
def get_summoner_data():
    region = request.args.get('region')
    summoner_name = request.args.get('summonerName')

    summoner_infos=get_summoner_infos(region,summoner_name)
    
    return json.dumps(summoner_infos)