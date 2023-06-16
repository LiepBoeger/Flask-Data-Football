from flask import Blueprint, render_template, request, redirect, url_for
from unicodedata import normalize
from translate import Translator
import requests

translator = Translator(to_lang='pt')
resultados_route_bp = Blueprint('resultados_route', __name__)
get_team_id_route_bp = Blueprint('get_team_id_route', __name__)
from app import all_teams

def traduz_cor(colors):
    cores_traduzidas = {}
    for color in colors:
        cor_traduzida = translator.translate(color)
        if color == 'Maroon':
            cor_traduzida = 'Vermelho' #Tradução vem errada, o Maroon acaba traduzindo para marrom.
        cores_traduzidas[color] = cor_traduzida
    return cores_traduzidas


@get_team_id_route_bp.route('/team_id', methods=['POST'])
def get_team_id():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_name = normalize('NFKD', team_name).encode('ASCII', 'ignore').decode('ASCII').title()
        for team in all_teams:
            if team['shortName'] == team_name:
                team_id = team['id']
                return redirect(url_for('resultados_route.resultados', team_id=team_id))
    return render_template('resultados_not_found.html')


@resultados_route_bp.route('/resultados/<team_id>', methods=['GET', 'POST'])
def resultados(team_id):
    headers = {
        'X-Auth-Token': '1ab307fb03544090b359c0d5c01577b4'
    }
    url = f'http://api.football-data.org/v4/teams/{team_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jsondata = response.json()
        colors = jsondata['clubColors'].split(' / ')
        cor_traduzida = traduz_cor(colors)
        competitions = jsondata.get('runningCompetitions', [])
        squad = jsondata.get('squad', [])
        return render_template('resultados.html', team=jsondata,
                               colors=cor_traduzida,
                               competitions=competitions,
                               squad=squad)
    return render_template('resultados_not_found.html')
