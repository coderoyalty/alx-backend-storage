#!/usr/bin/env python3
"""
8-all
"""


def list_all(mongo_collection):
    """
    list all documents of a mongo_collection
    """
    docs = mongo_collection.find()
    if docs.count() == 0:
        return []
    return docs
