from flask import current_app, Blueprint, jsonify
api = Blueprint('api', __name__)

@api.route("/")
def index():