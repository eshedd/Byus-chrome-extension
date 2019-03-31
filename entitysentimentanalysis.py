# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import statistics
import textwrap
import os
#import analyze
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import six
import argparse
import operator


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "Desktop/Ali/apps/POLO/Alathea/credentials.json"

entities = []
print ("something")

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
    print (entList)

    for entity in result.entities:
        entities.append(SentimentEntity(entity))
    print(entities)

text1 ="bad Google, headquartered in Mountain View, unveiled the new good google at google.  Sundar Pichai said in his keynote that users love their new googles."
entity_sentiment_text(text1)

top5 = sorted(entities, key=lambda k: k.salience, reverse=True)[:5]
print(top5)
print(top5[4].name)

i=0
while i <= 4 :
    print (i)
    if (top5[i].score >= -0.15) & (top5[i].score <= 0.15) & (top5[i].magnitude >= 3):
        print("This article views "+ top5[i].name +" in a neutral way and doesn't seemed biased on this topic.")
    if (top5[i].score  >= -0.15) & (top5[i].score  <= 0.15) & (top5[i].magnitude  <= 3):
        print("This article views "+ top5[i].name +" in a neutral way but it doesn't seem to include much information on this topic.")
    if (top5[i].score  <= -0.15):
        print("This article  seems to take a negatively stance on "+top5[i].name +" and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.")
    if (top5[i].score  >= 0.15):
        print("This article  seems to take a positive stance on "+top5[i].name +" and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.")
    i = i+1

entities[0].salience
entities[0].magnitude
entities[0].score
