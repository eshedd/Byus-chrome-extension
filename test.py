from flask import Flask, request, send_file, jsonify
from entitysentimentanalysis import entity_sentiment_text
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
#    client = language.LanguageServiceClient()
    toAnalyze = request.values.get('text')
#    document = types.Document(content = toAnalyze, type = enums.Document.Type.PLAIN_TEXT)
#    result = client.analyze_entities(document = document)
    result = entity_sentiment_text(toAnalyze)
#    result = json.loads(MessageToJson(result))
    entList = []
    for entity in result.entities:
        qualities = {}
        qualities['Name'] = '{}'.format(entity.name)
        for mention in entity.mentions:
            qualities['Magnitude'] = '{}'.format(mention.sentiment.magnitude)
            qualities['Sentiment'] = '{}'.format(mention.sentiment.score)
            qualities['Salience'] = '{}'.format(entity.salience)
            entList.append(qualities)
    return json.dumps(entList)