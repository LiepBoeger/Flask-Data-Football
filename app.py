from flask import Flask
from unicodedata import normalize
from routes import home_route, resultados_route
import requests

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret_key'
app.register_blueprint(home_route.home_route_bp)
app.register_blueprint(resultados_route.resultados_route_bp)
app.register_blueprint(resultados_route.get_team_id_route_bp)

headers = {
            'X-Auth-Token': '1ab307fb03544090b359c0d5c01577b4'
        }

url = 'http://api.football-data.org/v4/competitions/2013/teams'
response = requests.get(url, headers=headers)

def format_names(team_name):
    for team in team_name:
        team['shortName'] = normalize('NFKD', team['shortName']).encode('ASCII', 'ignore').decode('ASCII').title()

if response.status_code == 200:
    all_teams = response.json().get('teams', [])
    format_names(all_teams)

if __name__ == '__main__':
    app.run(debug=True)