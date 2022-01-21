from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort

app = Flask(__name__)

from app import views
from app import tree_views

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

