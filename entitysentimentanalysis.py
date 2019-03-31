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

import textwrap
import os
#import analyze
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys
import six

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/ethanshedd/Downloads/credentials.json"

print ("something")

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
    return result

#    for entity in result.entities:
        #print('Mentions: ')
#        print(u'Name: "{}"'.format(entity.name))
#        for mention in entity.mentions:
#            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
#            print(u'  Content : {}'.format(mention.text.content))
#            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
#            print(u'  Sentiment : {}'.format(mention.sentiment.score))
#            print(u'  Type : {}'.format(mention.type))
#        print(u'Salience: {}'.format(entity.salience))
text1 = "bad Google, headquartered in Mountain View, unveiled the new Android phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote that users love their new Android phones."
entity_sentiment_text(text1)