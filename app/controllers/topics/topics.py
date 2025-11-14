from . import topics_bp
from flask import jsonify   
import json


@topics_bp.route("/list", methods=["GET"])
def list_topics():
    with open("app/models/topics.json") as f:
        topics = json.load(f)
    return jsonify(topics), 200

@topics_bp.route("/get/<identifier>", methods=["GET"])
def get_topic(identifier):
    with open("app/models/topics.json") as f:
        topics = json.load(f)
    topic = topics.get(identifier)
    if topic:
        return jsonify({identifier: topic}), 200
    else:
        return jsonify({"error": "Topic not found"}), 404   
    