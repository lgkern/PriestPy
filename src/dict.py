import json
 
class DictionaryReader:
    
    def __init__(self):
        self.file = 'dictEntries.txt'
        self.dictionary = {}
        self.loadDict()
        self.loop = 0
        
    def loadDict(self):
        try:
            with open(self.file, 'r') as f:
                s = f.read()
                self.dictionary = json.loads(s)
        except Exception:
            return

    def whisperCommands(self):
        return self.dictionary["whisper"]
    
    def roles(self):
        return self.dictionary["roles"]

    def admins(self):
        return self.dictionary["authorized"]
        
    def logChannels(self):
        return self.dictionary["logchannels"]
    
    def sentCommands(self):
        return self.dictionary["sentcommands"]
        
    def actionLogChannel(self):
        return str(self.dictionary["actionLogChannel"])

    def readEntry(self, entry, channelName):
        self.loop = self.loop + 1
        if self.loop > 10:
            print("Loop error")
            return None
        fixed = self.fixEntry(entry)
        print(fixed)
        if "pawn.discipline" in fixed and len(fixed.split(".")) == 7:
            fixed = map(int,fixed.split(".")[2:])                                              
            fixed = self.getdiscstats(*fixed)
            return fixed
        if fixed in self.dictionary:
            while fixed in self.dictionary:
                fixed = self.dictionary[fixed]
            return fixed
        else:
            print(entry.split('.')[0]+".invalid")
            entryText = entry.split('.')[0] if isinstance(entry, str) else ''
            chName = channelName if isinstance(channelName, str) else ''
            return self.readEntry(entryText+"."+chName,chName)
            
    def getdiscstats(self,intellect,crit,haste,mastery,vers,blef=0):
        hasterating = 325
        critrating = 350
        masteryrating = 233.3333
        versrating = 400
        critpun = 1 #punishment for crit for being unreliable
        baseatonment = 0.75
        intellect = intellect + 1300  #flask
       
        intweight = 1000/((intellect/100)/1.05)
        hasteweight = intweight * 1.1
        basecrit = 0.05+(0,0.01)[blef]
        critweight = 1000*(critpun/critrating/(((((crit/critrating)/100+basecrit)*critpun)+1)))
        masteryweight = 1000*(1/masteryrating/((1+(mastery/masteryrating)/100)+0.12)*baseatonment)
        versweight = 1000*(1/versrating/(  1+(vers/versrating)/100))
        leechweight = 1000/300*0.75
        normint = str(round(intweight/intweight,2))
        normhaste = str(round(hasteweight/intweight,2))
        normcrit = str(round(critweight/intweight,2))
        normmastery = str(round(masteryweight/intweight,2))
        normvers = str(round(versweight/intweight,2))
        normleech = str(round(leechweight/intweight,2))
        #return "```( Pawn: v1: \"Disc raid\": Intellect =",normint,", Versatility =",normvers,", HasteRating = 1.1, MasteryRating =",normmastery,", CritRating =",normcrit,", Leech =",normleech,")```"
        return '```( Pawn: v1: \"Disc raid\": Intellect=' + normint+', Versatility='+normvers+', HasteRating='+normhaste+', MasteryRating='+normmastery+', CritRating='+normcrit+', Leech='+normleech+')```'


            
    def fixEntry(self, entry):
        result = entry.lower()
        #Head
        result = result.replace("helm","head",1)
        #Neck
        result = result.replace("amulet","neck",1)
        result = result.replace("necklace","neck",1)
        #Shoulder
        result = result.replace("shoulders","shoulder",1)
        #Cloak
        result = result.replace("cloak","back",1)
        #Chest
        result = result.replace("robe","chest",1)
        #Wrist
        result = result.replace("wrists","wrist",1)
        result = result.replace("bracer","wrist",1)
        result = result.replace("bracers","wrist",1)
        #Gloves
        result = result.replace("hands","gloves",1)
        #Waist
        result = result.replace("belt","waist",1)
        #Legs
        result = result.replace("leggings","legs",1)
        #Feet
        result = result.replace("boots","feet",1)
        result = result.replace("foot","neck",1)
        #Ring
        result = result.replace("finger","ring",1)
        #Trinket
        #Weapon
        #Off-hand
        
        #Specs
        if "ord" not in result:
            if "discipline" not in result:
                result = result.replace("disc","discipline",1)
        
        result = result.replace("pub.","",1)

        #Aliases
        result = result.replace("weakauras","wa",1)
        if "link" not in result:
            result = result.replace("lexicon","link.lexicon",1)
            result = result.replace("guide","link.guide",1)
            
        #TODO: Better logic
        
        result = result.replace("holy.artifact","artifact.holy",1)
        result = result.replace("shadow.artifact","artifact.shadow",1)
        result = result.replace("discipline.artifact","artifact.discipline",1)
        
        result = result.replace("holy.guide","artifact.guide",1)
        result = result.replace("shadow.guide","artifact.guide",1)
        result = result.replace("discipline.guide","artifact.guide",1)
        
    
        return result
        
    def commandReader(self, params, channelName = ''):
        self.loop = 0
        return self.readEntry('.'.join(params.split(' ')), channelName)

    def itemReader(self, params):
        self.loop = 0
        result = self.commandReader(params)
        if 'Invalid' in result:
            itemId = params.split(' ')[1]
            if itemId.isdigit():
                return 'https://wowhead.com/item='+itemId
        return result