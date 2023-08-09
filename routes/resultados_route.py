from flask import Blueprint, render_template, request, redirect, url_for, session
from unicodedata import normalize
from translate import Translator
import requests

translator = Translator(to_lang='pt')
resultados_route_bp = Blueprint('resultados_route', __name__)
get_team_id_route_bp = Blueprint('get_team_id_route', __name__)
from app import all_teams

def traduz_cor(colors):
    cores_traduzidas = {color: translator.translate(color) for color in colors}
    key = 'Maroon'
    if key in cores_traduzidas:
        cores_traduzidas['Maroon'] = 'Vermelho'
    return cores_traduzidas

@get_team_id_route_bp.route('/team_id', methods=['POST'])
def get_team_id():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_name = normalize('NFKD', team_name).encode('ASCII', 'ignore').decode('ASCII').title()

        team_id = next((team['id'] for team in all_teams if team['shortName'] == team_name), None)
        if team_id:
            session['team_id'] = team_id
            return redirect(url_for('resultados_route.resultados', team_id=team_id))
        return render_template('resultados_not_found.html')

@resultados_route_bp.route('/resultados/<team_id>', methods=['GET', 'POST'])
def resultados(team_id):
    if session['team_id'] == team_id:
        jsondata = session.get('team_data')
    else:
        headers = {'X-Auth-Token': '1ab307fb03544090b359c0d5c01577b4'}
        url = f'http://api.football-data.org/v4/teams/{team_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            jsondata = response.json()
            session['team_id'] = team_id
            session['team_data'] = jsondata
        else:
            return render_template('resultados_not_found.html')

    colors = jsondata['clubColors'].split(' / ')
    cor_traduzida = traduz_cor(colors)
    competitions = jsondata.get('runningCompetitions', [])
    squad = jsondata.get('squad', [])
    coach = jsondata.get('coach')

    jogadores_por_posicao = {}
    for jogador in jsondata['squad']:
        posicao = translator.translate(jogador['position'])
        if posicao == 'Transgressão':
            posicao = 'Atacante'
        if posicao == 'meio de campo':
            posicao = 'Meio-Campo'
        if posicao not in jogadores_por_posicao:
            jogadores_por_posicao[posicao] = []
        jogadores_por_posicao[posicao].append(jogador)

    return render_template('resultados.html', team=jsondata,
                           colors=cor_traduzida,
                           competitions=competitions,
                           squad=squad,
                           coach=coach,
                           jogadores_por_posicao=jogadores_por_posicao)
