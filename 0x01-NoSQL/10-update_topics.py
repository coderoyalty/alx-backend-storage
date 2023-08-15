#!/usr/bin/env python3
"""
10-update_topics
"""


def update_topics(mongo_collection, name, topics):
    """
    update topics
    """
    query = {"name": name}
    update = {"$set": {
        "topics": topics
    }}

    mongo_collection.update_many(query, update)
