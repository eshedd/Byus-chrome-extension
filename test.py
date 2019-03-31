from flask import Flask, request, send_file, jsonify
from google.protobuf.json_format import MessageToJson 
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import json

import statistics
import textwrap
import sys
import six
import argparse
import operator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/ethanshedd/Downloads/credentials.json"

class SentimentEntity:
    def __init__(self, entity):
        self.entity = entity
        self.name = entity.name
        self.mentions = entity.mentions
        self.magnitude = statistics.mean([mention.sentiment.magnitude for mention in entity.mentions])
        self.score = statistics.mean([mention.sentiment.score for mention in entity.mentions])
        self.salience = entity.salience
    def __repr__(self):
        return self.name

def entity_sentiment_text(text):
    results = ""
    entities = []
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)
    entList = []
    for entity in result.entities:
        for mention in entity.mentions:
            qualities = {}
            qualities['Content'] = '{}'.format(mention.text.content)
            qualities['Magnitude'] = '{}'.format(mention.sentiment.magnitude)
            qualities['Sentiment'] = '{}'.format(mention.sentiment.score)
            qualities['Type'] = '{}'.format(mention.type)
            qualities['Salience'] = '{}'.format(entity.salience)
            entList.append(qualities)
#    print (entList)

    for entity in result.entities:
        entities.append(SentimentEntity(entity))
#    print(entities)
    top5 = sorted(entities, key=lambda k: k.salience, reverse=True)[:5]
    i=0
    while i < len(top5) :
        print (i)
        if (top5[i].score >= -0.15) & (top5[i].score <= 0.15) & (top5[i].magnitude >= 3):
            results += ("This article views "+ top5[i].name +" in a neutral way and doesn't seemed biased on this topic.\n")
        if (top5[i].score  >= -0.15) & (top5[i].score  <= 0.15) & (top5[i].magnitude  <= 3):
            results += ("This article views "+ top5[i].name +" in a neutral way but it doesn't seem to include much information on this topic.\n")
        if (top5[i].score  <= -0.15):
            results += ("This article  seems to take a negatively stance on "+top5[i].name +" and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.\n")
        if (top5[i].score  >= 0.15):
            results += ("This article  seems to take a positive stance on "+top5[i].name +" and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.\n")
        i = i+1
    entList = []
    for entity in result.entities:
        for mention in entity.mentions:
            qualities = {}
            qualities['Magnitude'] = '{}'.format(mention.sentiment.magnitude)
            qualities['Sentiment'] = '{}'.format(mention.sentiment.score)
            qualities['Salience'] = '{}'.format(entity.salience)
            entList.append(qualities)
    return json.dumps(entList) + "\n" + results

app = Flask(__name__)
@app.route("/")
def home():
    return send_file('popup.html')
@app.route("/analyze")
def test():
    print("added to test")
#    client = language.LanguageServiceClient()
    toAnalyze = request.values.get('text')
#    document = types.Document(content = toAnalyze, type = enums.Document.Type.PLAIN_TEXT)
#    result = client.analyze_entities(document = document)
    result = entity_sentiment_text(toAnalyze)
#    result = json.loads(MessageToJson(result))
    
    return result