from flask import Blueprint, render_template, request, redirect, url_for
import requests

resultados_route_bp = Blueprint('resultados_route', __name__)
get_team_id_route_bp = Blueprint('get_team_id_route', __name__)
from app import all_teams

@get_team_id_route_bp.route('/team_id', methods=['POST'])
def get_team_id():
    if request.method == 'POST':
        team_name = request.form['team_name']

        for team in all_teams:
            if team['name'] == team_name:
                team_id = team['id']
                return redirect(url_for('resultados_route.resultados', team_id=team_id))
        return render_template('resultados.html', team='Time não encontrado')

@resultados_route_bp.route('/resultados/<team_id>', methods=['GET', 'POST'])
def resultados(team_id):
    headers = {
        'X-Auth-Token': '1ab307fb03544090b359c0d5c01577b4'
    }
    url = f'http://api.football-data.org/v4/teams/{team_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jsondata = response.json()
        return render_template('resultados.html', team=jsondata)
    return render_template('resultados.html', team='Time não encontrado')
