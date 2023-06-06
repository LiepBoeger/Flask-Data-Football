from flask import Flask
from routes import home_route, resultados_route
import requests

app = Flask(__name__, static_folder='static')
app.register_blueprint(home_route.home_route_bp)
app.register_blueprint(resultados_route.resultados_route_bp)
app.register_blueprint(resultados_route.get_team_id_route_bp)

headers = {
            'X-Auth-Token': '1ab307fb03544090b359c0d5c01577b4'
        }

url = 'http://api.football-data.org/v4/teams/'
response = requests.get(url, headers=headers)
if response.status_code == 200:
    all_teams = response.json().get('teams', [])

if __name__ == '__main__':
    app.run(debug=True)