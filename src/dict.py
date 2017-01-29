import json
import requests
from botkey import Key

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
        if "pawn.discipline" in fixed and len(fixed.split(".")) >= 5:
            fixed = fixed.split(".")[2:]
            charname = fixed[0]
            charrealm = "-".join(fixed[1:-1])
            charzone = fixed[-1]
            fixed = self.getcharstats(charname,charrealm,charzone)
            fixed = self.getdiscstats(*fixed)
            return fixed
        if "cmd" in fixed and len(fixed.split(".")) >= 4:
            if len(fixed.split(".")) > 4:
                food = fixed[3]  
            else:
                food = None
            fixed = fixed.split(".")[1:]
            charname = fixed[0]
            charrealm = "-".join(fixed[1:-1])
            charzone = fixed[2]
            fixed = self.getShadowCharStats(charname,charrealm,charzone)
            fixed = self.getCMDratioResponse(*fixed,food)
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
    
    def getcharstats(self,name,realm,zone):
        zone = zone.lower()
        locales = {"us":"en_US","eu":"en_GB","kr":"ko_KR","tw":"zh_TW"}
        locale = locales[zone]
        url = "https://"+zone+".api.battle.net/wow/character/"+realm+"/"+name+"?fields=stats&locale="+locale+"&apikey="+Key().bnetApiKey()
        r = requests.get(url)
        response = r.json()
        blelfworg = (0,1)[response["race"] == 10 or response["race"] == 22]
        taurdwarf = (0,1)[response["race"] == 6 or response["race"] == 3]
        charint = response["stats"]["int"]
        charcrit = response["stats"]["critRating"]
        charhaste = response["stats"]["hasteRating"]
        charmastery = response["stats"]["masteryRating"]
        charvers = response["stats"]["versatility"]
        url = "https://"+zone+".api.battle.net/wow/character/"+realm+"/"+name+"?fields=items&locale="+locale+"&apikey="+Key().bnetApiKey()
        r = requests.get(url)
        response = r.json()
        drape = (0,1)[response["items"]["back"]["name"] == "Drape of Shame"]
       
        return [charint,charcrit,charhaste,charmastery,charvers,blelfworg,taurdwarf,drape]
        
    def getShadowCharStats(self,name,realm,zone):
        zone = zone.lower()
        locales = {"us":"en_US","eu":"en_GB","kr":"ko_KR","tw":"zh_TW"}
        locale = locales[zone]
        url = "https://"+zone+".api.battle.net/wow/character/"+realm+"/"+name+"?fields=stats&locale="+locale+"&apikey="+Key().bnetApiKey()
        r = requests.get(url)
        response = r.json()
        extracrit = (0,1)[response["race"] == 10 or response["race"] == 22 or response["race"] == 4]        
        extrafood = (0,1)[response["race"] == 24 or response["race"] == 25 or response["race"] == 26]
        charint = response["stats"]["int"]
        charcrit = response["stats"]["critRating"]
        charhaste = response["stats"]["hasteRating"]
        charmastery = response["stats"]["masteryRating"]
        charvers = response["stats"]["versatility"]
               
        return [charint,charcrit,charhaste,charmastery,charvers,extracrit,extrafood]
   
    def getdiscstats(self,intellect,crit,haste,mastery,vers,blef=0,tauren=0,drape=0):
        hasterating = 375
        critrating = 400   
        masteryrating = 266.66666
        versrating = 475
        critpun = 1+(0,0.1)[drape]+(0,0.02)[tauren]
        raidatone = 0.75
        dungeonatone = 0.45
        intellect = intellect + 1706
        intweight = 1000/((intellect/100)/1.05)
        basecrit = 0.05+(0,0.01)[blef]
        critweight = 1000*((critpun)/critrating/(((((crit/critrating)/100+basecrit)*(critpun))+1)))
        raidmasteryweight = 1000*(1/masteryrating/((1+(mastery/masteryrating)/100)+0.12)*raidatone)
        dungeonmasteryweight = 1000*(1/masteryrating/((1+(mastery/masteryrating)/100)+0.12)*dungeonatone)
        versweight = 1000*(1/versrating/(  1+(vers/versrating)/100))
        hasteweight = max(critweight,raidmasteryweight,versweight)  * 1.1
        leechweight = 1000/300*0.75
        dungleech = 1000/300*0.75/2
        normint = str(round(intweight/intweight,2))
        normhaste = str(round(hasteweight/intweight,2))
        normcrit = str(round(critweight/intweight,2))
        raidnormmastery = str(round(raidmasteryweight/intweight,2))
        dungeonnormmastery = str(round(dungeonmasteryweight/intweight,2))
        normvers = str(round(versweight/intweight,2))
        normleech = str(round(leechweight/intweight,2))
        normdungleech = str(round(dungleech/intweight,2))
        return '```( Pawn: v1: \"Disc Raid\": Intellect=' + normint+', Versatility='+normvers+', HasteRating='+normhaste+', MasteryRating='+raidnormmastery+', CritRating='+normcrit+', Leech='+normleech+')```\
```( Pawn: v1: \"Disc Dungeon\": Intellect=' + normint+', Versatility='+normvers+', HasteRating='+normhaste+', MasteryRating='+dungeonnormmastery+', CritRating='+normcrit+', Leech='+normdungleech+')```'

    def getCMDratioResponse(self,intellect,crit,haste,mastery,vers,extracrit=0,extrafood=0,food=None):
        if not food:
            if extracrit == 0 and extrafood == 0:
                return 'Crit Rating: '+str(crit)+'\nMastery Rating: '+str(mastery)+'(+375 from Food)\nCMD Ratio: '+'{0:.2f}'.format(crit/(crit+mastery+375))+'\nMore info: https://howtopriest.com/viewtopic.php?f=60&t=9734'
            if extracrit == 1:
                return 'Crit Rating: '+str(crit)+'(+400 from Racial)\nMastery Rating: '+str(mastery)+'(+375 from Food)\nCMD Ratio: '+'{0:.2f}'.format((crit+400)/(crit+400+mastery+375))+'\nMore info: https://howtopriest.com/viewtopic.php?f=60&t=9734'
            if extrafood == 1:
                return 'Crit Rating: '+str(crit)+'\nMastery Rating: '+str(mastery)+'(+750 from Food)\nCMD Ratio: '+'{0:.2f}'.format((crit)/(crit+mastery+750))+'\nMore info: https://howtopriest.com/viewtopic.php?f=60&t=9734'
        else:
            if extracrit == 0 and extrafood == 0:
                return 'Crit Rating: '+str(crit)+'\nMastery Rating: '+str(mastery)+'\nCMD Ratio: '+'{0:.2f}'.format(crit/(crit+mastery))+'\nMore info: https://howtopriest.com/viewtopic.php?f=60&t=9734'
            if extracrit == 1:
                return 'Crit Rating: '+str(crit)+'(+400 from Racial)\nMastery Rating: '+str(mastery)+'\nCMD Ratio: '+'{0:.2f}'.format((crit+400)/(crit+400+mastery+375))+'\nMore info: https://howtopriest.com/viewtopic.php?f=60&t=9734'        
        
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
