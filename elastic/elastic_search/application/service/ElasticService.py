import os
import logging
import time
import elasticsearch.exceptions as exception
from elastic_search.utils.ElasticQuery import ElasticQuery
from elasticsearch import Elasticsearch
from elastic_search.config.config import INDEX,ELASTIC,PARAM
logging.getLogger().setLevel(logging.INFO)


class ElasticService:
    def __init__(self) -> None:
        self._url = ELASTIC["url"]
        self._es_client = Elasticsearch([self._url],timeout=1)
        self.index_name= INDEX["name"]

    def search_product(self):
        """

        :param query:
        :return:
        """
        max_retries = PARAM["max_retries"]
        retries = 0
        while retries < max_retries:
            try:
                list_product=[]
                page_size = 10000
                query= ElasticQuery.distinct_product()
                response = self._es_client.search(index=self.index_name, size=page_size,body=query)
                response_bucket = response["aggregations"]["distinct_product_ids"]["buckets"]
                if response_bucket:
                    for bucket in response_bucket:
                        list_product.append(bucket["distinct_docs"]["hits"]["hits"][0]["_source"])
                    return list_product
                else:
                    raise exception.NotFoundError("No value returned from query..")
            except exception.ConnectionError as ex:
                logging.error(f"Connection issue on elasticsearch. Retrying")
                retries += 1
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

    def search_product_details(self,product_id):
        """

        :param product_id:
        :param query:
        :return:

        """
        max_retries = PARAM["max_retries"]
        retries = 0
        while retries < max_retries:
            try:
                product=[]
                page_size = 10000
                query = ElasticQuery.product_category(product_id)
                response = self._es_client.search(index=self.index_name, size=page_size,body=query)
                if response['hits']['hits']:
                    product_details = response['hits']['hits']
                    if product_details:
                        for product_detail in product_details:
                            product.append(product_detail["_source"])
                        return product
                logging.error("no response found")
                raise exception.NotFoundError("No value returned from query..")

            except exception.ConnectionError as ex:
                logging.error(f"Connection issue on elasticsearch. Retrying")
                retries += 1
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

    def search_in_index(self,parameter):
        """

        :param parameter:
        :param query:
        :return:
        """
        max_retries = PARAM["max_retries"]
        retries = 0
        while retries < max_retries:
            try:
                list_item=[]
                page_size = 10000
                query = ElasticQuery.search(parameter)
                response = self._es_client.search(index=self.index_name, size=page_size,body=query)
                item_details= response['hits']['hits']
                if item_details:
                    for item in item_details:
                        list_item.append(item["_source"])
                    return list_item
                else:
                    return "Search item not found"

            except exception.ConnectionError as ex:
                logging.error(f"Connection issue on elasticsearch with exception {ex}. Retrying")
                retries += 1
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex


elastic_service = ElasticService()






k= ElasticService().search_product_details("201816")
print(k)