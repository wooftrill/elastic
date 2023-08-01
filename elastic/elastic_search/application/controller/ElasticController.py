import os
import logging
from elastic_search.application.service.ElasticService import ElasticService,elastic_service
from elastic_search.application.model.Error import Error
from elastic_search.application.model.ElasticModel import ElasticModel
from http import HTTPStatus
from flask import jsonify, make_response,request
from elastic_search.application import app


logging.getLogger().setLevel(logging.INFO)


class ElasticController:
    def __init__(self,s: ElasticService):
        self.service = s


elastic_controller = ElasticController(elastic_service)


@app.get('/')
def welcome():
    return "Welcome to service"


@app.get('/get_subcategory_name',endpoint='get_subcategory_name')
def get_subcategory_name():
    try:
        response = elastic_controller.service.search_subcategory()
        if response:
            return make_response(jsonify(message=response), HTTPStatus.OK)
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)
        error = Error(message="Internal Server Error", type="500", message_id=HTTPStatus.CONFLICT)
        return make_response(jsonify(error, HTTPStatus.INTERNAL_SERVER_ERROR))


@app.get('/get_products',endpoint='get_products')
def get_product():
    try:
        param = request.args['subcategory_name']
        query_param = ElasticModel(param)
        print(query_param.query)
        response = elastic_controller.service.search_product(query_param.query)
        if response:
            return make_response(jsonify(message=response), HTTPStatus.OK)
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)
        error = Error(message="Internal Server Error", type="500", message_id=HTTPStatus.CONFLICT)
        return make_response(jsonify(error, HTTPStatus.INTERNAL_SERVER_ERROR))


@app.get('/get_product_details',endpoint='get_product_details')
def get_product_details():
    try:
        product_id = request.args['product_id']
        query_param= ElasticModel(product_id)
        response = elastic_controller.service.search_product_details(query_param.query)
        if response:
            return make_response(jsonify(message=response), HTTPStatus.OK)
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)
        error = Error(message="Internal Server Error", type="500", message_id=HTTPStatus.CONFLICT)
        return make_response(jsonify(error, HTTPStatus.INTERNAL_SERVER_ERROR))


@app.get('/search_item_details',endpoint='search_item_details')
def search_item_details():
    try:
        param = request.args['search_string']
        query_param= ElasticModel(param)
        response = elastic_controller.service.search_in_index(query_param.query)
        if response:
            return make_response(jsonify(message=response), HTTPStatus.OK)
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)
        error = Error(message="Internal Server Error", type="500", message_id=HTTPStatus.CONFLICT)
        return make_response(jsonify(error, HTTPStatus.INTERNAL_SERVER_ERROR))


