from flask import Blueprint, render_template

home_route_bp = Blueprint('home_route', __name__)

@home_route_bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')