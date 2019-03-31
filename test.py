from flask import Flask, request, send_file, jsonify
from google.protobuf.json_format import MessageToJson 
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/ethanshedd/Downloads/credentials.json"

app = Flask(__name__)
@app.route("/")
def home():
    return send_file('popup.html')
@app.route("/analyze")
def test():
    client = language.LanguageServiceClient()
    toAnalyze = request.values.get('text')
    document = types.Document(content = toAnalyze, type = enums.Document.Type.PLAIN_TEXT)
    result = client.analyze_entities(document = document)
    result = json.loads(MessageToJson(result))
    entities = []
    for entity in result['entities']:
        entities.append(entity['name'] + " : " + entity['type'])
    return jsonify(entities)