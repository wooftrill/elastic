import os
import logging

logging.getLogger().setLevel(logging.INFO)


class ElasticQuery:

    @staticmethod
    def distinct_subcategory():
        query = {
            "size": 0,
            "aggs": {
                "distinct_subcategory_names": {
                    "terms": {
                        "field": "subcategory_name.keyword",
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
    def distinct_product_wrt_subcategory_name(subcategory_name):
        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "subcategory_name.keyword": subcategory_name
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "distinct_product_ids": {
                    "terms": {
                        "field": "product_id.keyword",
                        "size": 10
                    },
                    "aggs": {
                        "top_product_hits": {
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






