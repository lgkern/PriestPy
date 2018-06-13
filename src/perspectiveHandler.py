from dict import DictionaryReader
from googleapiclient import discovery
from botkey import Key
from discord import TextChannel
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

        #print(json.dumps(body, indent=2))

        response = service.comments().analyze(body=body).execute()

        #print(json.dumps(response, indent=2))

        if response is not None:            
            score = response['attributeScores']['TOXICITY']['summaryScore']['value']

            source = message.channel.name if isinstance(message.channel, TextChannel) else 'PM'        

            if float(score) > 0.85:
                await client.get_channel(int(p.perspectiveLogChannelH2P())).send('Toxic Message Warning - {0:.2g}% Toxicity - on {2} from {1.author}({1.author.id})```{1.content}```'.format(score * 100.0, message, source))

    # Creates a JSON with all attributes requested
    def buildAttributes(self, attributes):
        result = ''

        for attribute in attributes:
            result += self.attributesBase.format(attribute)

        return result

    def buildRequest(self, message, attributes):

        return {'comment': { 'text': message }, 'requestedAttributes': {'TOXICITY': {}} }

    async def addReactions(self, dictionary, message):
        emojiList = dictionary.perspectiveReactions()

        for emoji in emojiList:
            #print(emoji)
            await message.add_reaction(emoji)

    async def feedback(self, reaction, user, dictionary):
        if reaction.emoji in dictionary.perspectiveReactions():
            # Find out the ranking based on the emoji 
            # Report the score
