import config
import configparser
from flask_cors import CORS
from apiflask import APIFlask

app = APIFlask(__name__,title="elastic_api_wt",version='1.0.0',spec_path='/spec')
cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
from elastic_search.application.controller.ElasticController import ElasticController