import os
import logging

logging.getLogger().setLevel(logging.INFO)


class ElasticQuery:

    @staticmethod
    def distinct_product():
        query={
            "size": 0,
            "aggs": {
                "distinct_product_ids": {
                    "terms": {
                        "field": "product_id.keyword",
                        "size": 10
                    },
                    "aggs": {
                        "distinct_docs": {
                            "top_hits": {
                                "size": 1
                            }
                        }
                    }
                }
            }
        }
        return query

    @staticmethod
    def product_category(product_id):
        query = {
            "query": {
                "match": {
                    "product_id": product_id
                }
            }
        }
        return query

    @staticmethod
    def search(param):
        query={
            "query": {
                "simple_query_string" : {
                    "query": param,
                        "fields": ["vendor_name", "product_name","subcategory_name","category_name","product_description"],
                            "default_operator": "and"
                             }
                            }
        }
        return  query




