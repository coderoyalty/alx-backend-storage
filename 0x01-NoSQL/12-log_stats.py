#!/usr/bin/env python3
"""
12-log_stats
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    no_logs = collection.count_documents({})
    print(f"{no_logs} logs")
    methods = ("GET", "POST", "PUT", "PATCH", "DELETE")
    print("Methods:")
    for method in methods:
        no_method = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {no_method}")

    status_check = collection.count_documents({
        "method": "GET", "path": "/status"
    })
    print(f"{status_check} status check")

    client.close()
