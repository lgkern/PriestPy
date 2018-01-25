from dict import DictionaryReader
from googleapiclient import discovery
from botkey import Key
import json
import logging


class PerspectiveHandler:

    def __init__(self):        
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        self.bodyBase = '{{comment: {{text: "{0}"}}, languages: ["en"], requestedAttributes: {{ {1} }} }}'
        self.analyze_request = {'comment': { 'text': 'friendly greetings from python' }, 'requestedAttributes': {'TOXICITY': {}} }
        self.attributesBase = '"{0}": {{}},'        
        self.defaultAttributes = [ 'TOXICITY' ]

    async def measure(self, client, message):
        p = DictionaryReader()
        service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=Key().perspectiveApiKey())
        
        body = self.buildRequest(message.content, self.buildAttributes(self.defaultAttributes))

        print(json.dumps(body, indent=2))

        response = service.comments().analyze(body=body).execute()

        print(json.dumps(response, indent=2))

        if response is not None:            
            score = response['attributeScores']['TOXICITY']['summaryScore']['value']

            if float(score) > 0.5:
                await client.get_channel(int(p.perspectiveLogChannel())).send('Toxic Message Warning - {0:.2g}% Toxicity - from {1.author}({1.author.id})```{1.content}```'.format(score * 100.0, message))

    # Creates a JSON with all attributes requested
    def buildAttributes(self, attributes):
        result = ''

        for attribute in attributes:
            result += self.attributesBase.format(attribute)

        return result

    def buildRequest(self, message, attributes):

        return {'comment': { 'text': message }, 'requestedAttributes': {'TOXICITY': {}} }