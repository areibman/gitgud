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
        # if data['gameDuration'] > 1200:
            json_array.append(data)
        # else:
        #     os.remove('game_dumps/'+str(data['gameId'])+'.json')
        #     print('removed-'+str(data['gameId'])+'.json')

    return json.dumps(json_array)

@app.route('/summoner-data')
def get_summoner_data():
    region = request.args.get('region')
    summoner_name = request.args.get('summonerName')

    summoner_infos=get_summoner_infos(region,summoner_name)
    
    return [
        {key: 'goldRow1',svgs: ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100"> <defs> <g id="src" opacity="0.5" fill="none" stroke-width="12"> <circle cx="-20" cy="19" r="1"/> <path d="M0,19s0-20-20-20m0-19s40,0,40,40" stroke-linecap="round"/> </g> </defs> <use xlink:href="#src" transform="translate(64,56) rotate(240)" stroke="#44F"/> <use xlink:href="#src" transform="translate(42,36) rotate(120)" stroke="#0C0"/> <use xlink:href="#src" transform="translate(35,65)" stroke="#F00"/></svg>']},
        {key: 'goldRow2',svgs: ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100"> <defs> <g id="src" opacity="0.5" fill="none" stroke-width="12"> <circle cx="-20" cy="19" r="1"/> <path d="M0,19s0-20-20-20m0-19s40,0,40,40" stroke-linecap="round"/> </g> </defs> <use xlink:href="#src" transform="translate(64,56) rotate(240)" stroke="#44F"/> <use xlink:href="#src" transform="translate(42,36) rotate(120)" stroke="#0C0"/> <use xlink:href="#src" transform="translate(35,65)" stroke="#F00"/></svg>','<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100"> <defs> <g id="src" opacity="0.5" fill="none" stroke-width="12"> <circle cx="-20" cy="19" r="1"/> <path d="M0,19s0-20-20-20m0-19s40,0,40,40" stroke-linecap="round"/> </g> </defs> <use xlink:href="#src" transform="translate(64,56) rotate(240)" stroke="#44F"/> <use xlink:href="#src" transform="translate(42,36) rotate(120)" stroke="#0C0"/> <use xlink:href="#src" transform="translate(35,65)" stroke="#F00"/></svg>']},
        {key: 'goldRow3',svgs: ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100"> <defs> <g id="src" opacity="0.5" fill="none" stroke-width="12"> <circle cx="-20" cy="19" r="1"/> <path d="M0,19s0-20-20-20m0-19s40,0,40,40" stroke-linecap="round"/> </g> </defs> <use xlink:href="#src" transform="translate(64,56) rotate(240)" stroke="#44F"/> <use xlink:href="#src" transform="translate(42,36) rotate(120)" stroke="#0C0"/> <use xlink:href="#src" transform="translate(35,65)" stroke="#F00"/></svg>']}
        ]