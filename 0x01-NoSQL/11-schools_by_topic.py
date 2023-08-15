#!/usr/bin/env python3
"""
11-schools_by_topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    schools by topic
    """
    return list(mongo_collection.find({"topics": topic}))
