import json
import requests
from math import pow
from botkey import Key

def armoryImport(self, player, realm, zone):
    #Realm and player name are supplied by the user.
    api_key = Key().bnetApiKey()
    locales = {"us":"en_US","eu":"en_GB","kr":"ko_KR","tw":"zh_TW"}
    locale = locales[zone]

    itemReport = ("https://us.api.battle.net/wow/character/"
                  + realm +"/"
                  + player
                  + "?fields=items&"
                  + "locale=" + locale
                  + "&apikey=" + api_key)


    r = requrests.get(itemReport)
    data = r.json()

    #Declare all the stats that matter and set to 0.
    intStat = 0
    critStat = 0
    mastStat = 0
    hasteStat = 0
    versStat = 0
    leechStat = 0

    #Set all the items up.
    slots = ["head","neck","shoulder","back","chest","wrist","hands","waist","legs","feet","finger1","finger2","trinket1","trinket2"]

    stats = {"versatility":0,
             "haste":0,
             "crit":0,
             "mastery":0,
             "intellect":0,
             "leech":0   }

    statsMap = {40:"versatility",
                36:"haste",
                32:"crit",
                49:"mastery",
                5:"intellect",
                71:"intellect",
                62:"leech"}

    for piece in slots:
        for attribute in data["items"][piece]["stats"]:
            stats[statsMap[attribute["stat"]]] += attribute["amount"]

    mainHand = slots["mainHand"]

    #Special Handling for the Artifact Weapon
    mainHandIlvl = mainHand["itemLevel"]

    #Use a 951 Artifact Weapon as a reference
    referenceInt = 22531
    referenceHaste = 1001
    referenceMast = 1001

    calcInt = round((referenceInt * (pow(1.15,((mainHandIlvl-951)/15)))))
    calcHaste = round(referenceHaste * (pow(1.15, (mainHandIlvl-951)/15) * pow(0.994435486,(mainHandIlvl-951))))
    calcMast = calcHaste

    #Add calculated artifact stats to total stats.
    intStat += calcInt
    hasteStat += calcHaste
    mastStat += calcMast

    #Add base int
    intStat += 7328

    #Factor in cloth int bonus
    intStat *= 1.05
    return[intStat,critStat,hasteStat,mastStat,versStat,leechStat,mainHandIlvl]

def armoryPawnAndNlcString(self,intStat,critStat,hasteStat,mastStat,versStat,leechStat,mainHandIlvl):
    #Atonement Healing contribution
    atonementHealPercent = 0.7

    #Haste Percent
    hastePercent = hasteStat/475/100

    #Calculated Pawn values
    pawnInt = round((1000/(intStat/100)/1.05),2)
    pawnCrit = round((1000/400/(1+(critStat/400/100 + 0.05))),2)
    pawnMastery = round((1000/250/(1+(mastStat/250/100))*atonementHealPercent),2)
    pawnVers = round((1000/475/(1+(versStat/475/100))),2)
    pawnHaste = round(max(pawnCrit,pawnMastery,pawnVers)*1.25/(1+hastePercent),2)
    pawnLeech = round(1000/460/(1+(leechStat/230/100)),2)

    #Average Concoordance Uptime
    concUptime = 0.33

    #Disc damage reduction for NLC traits
    dmgReduc = 0.45

    #Use a 951 Artifact Weapon as a reference
    referenceInt = 22531
    referenceHaste = 1001
    referenceMast = 1001

    intDiff = round((referenceInt * (pow(1.15,((mainHandIlvl-951)/15)))))
    hasteDiff = round(referenceHaste * (pow(1.15, (mainHandIlvl-951)/15) * pow(0.994435486,(mainHandIlvl-951))))
    mastDiff = calcHaste

    #Setup PP values for +1 to artifact and NLC Traits
    plusOne = round(intDiff * pawnInt + hasteDiff * pawnHaste + mastDiff * pawnMastery,2)
    masterOfShadows = round(500 * pawnMastery)
    lightSpeed = round(500 * pawnHaste)
    chaoticDarkness = round(180000 * (2 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    infusionOfLight = round(101000 * (4 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    shadowBind = round(200000 * (2 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    tormentTheWeak = round(80000 * 4 * dmgReduc * atonementHealPercent,2)
    secureInTheLight = round(135000 * (3 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    darkSorrows = round(127066 * (1 * (1 + hastePercent)) * dmgReduc * atonementHealPercent,2)
    murderousIntent = round(1500 * concUptime * pawnVers,2)
    shockLight = round(1500 * concUptime * pawnCrit,2)
    refractiveShell = round(300000 * (2 * (1 + hastePercent)) / 60 / 20,2)
    lightsEmbrace = round(45500 * 8 / 60 / 20,2)


    #Generate the Value of each relic
    roundplusOneValue = 1
    masterOfShadows /= plusOne
    lightSpeed /= plusOne
    chaoticDarkness /= plusOne
    infusionOfLight /= plusOne
    shadowBind /= plusOne
    tormentTheWeak /= plusOne
    secureInTheLight /= plusOne
    darkSorrows /= plusOne
    murderousIntent /= plusOne
    shockLight /= plusOne
    refractiveShell /= plusOne
    lightsEmbrace /= plusOne

    #Round everything to 2 decimal points
    roundplusOneValue = round(lightsEmbrace,2)
    masterOfShadows = round(masterOfShadows,2)
    lightSpeed = round(lightSpeed,2)
    chaoticDarkness = round(chaoticDarkness,2)
    infusionOfLight = round(infusionOfLight,2)
    shadowBind = round(shadowBind,2)
    tormentTheWeak = round(tormentTheWeak,2)
    secureInTheLight = round(secureInTheLight,2)
    darkSorrows = round(darkSorrows,2)
    murderousIntent = round(murderousIntent,2)
    shockLight = round(shockLight,2)
    refractiveShell = round(refractiveShell,2)
    lightsEmbrace = round(lightsEmbrace,2)

    #Percent of healing values from Various Logs
    penance = 0.3
    pws = 0.0956
    edge = 0.0677
    bol = 0.055
    lr = 1.2575

    #Calculate Relic Values
    confession = penance * 0.04 * 100
    shieldOfFaith = pws * 0.05 * 100
    edgeOfDarkAndLight = edge * 0.05 * 100
    burstOfLight = bol * 0.05 * 100
    leniencesReward = round(lr,2)

    #Pawn String
    pawnString = ('```( Pawn: v1: "Disc Sheet": Class=Priest, Spec=Discipline,'
                 + 'Intellect=' + str(pawnInt)
                 + ',Leech= ' + str(pawnLeech)
                 + ',HasteRating= ' + str(pawnHaste)
                 + ',MasteryRating= ' + str(pawnMastery)
                 + ',Versatility= ' + str(pawnVers)
                 + ',CritRating= ' + str(pawnCrit)
                 +  ')```' )


    #NLC String
    nlcString = ('Crucible Weights String: ```cruweight^128868^'
             '197716^' + str(burstOfLight) + '^'
             '252191^' + str(murderousIntent) + '^'
             '238063^' + str(leniencesReward) +  '^'
             '216212^0^'
             '252207^' + str(refractiveShell) + '^'
             '197713^0^'
             '252091^' + str(masterOfShadows) + '^'
             '197729^' + str(shieldOfFaith) + '^'
             '253111^' + str(lightsEmbrace) + '^'
             '252875^' + str(shadowBind) + '^'
             'ilvl^1.00^'
             '197727^^'
             '197711^0^'
             '252922^' + str(darkSorrows) + '^'
             '197715^' + str(edgeOfDarkAndLight) +  '^'
             '252088^' + str(lightSpeed) + '^'
             '252906^' + str(tormentTheWeak) + '^'
             '253093^' + str(infusionOfLight) + '^'
             '197762^0.01 ^'
             '253070^' + str(secureInTheLight) + '^'
             '252888^' + str(chaoticDarkness) + '^'
             '252799^0^'
             '197708^1^end```'	)
    return (pawnString + '\n' + nlcString)

def wclBossSelector(self,rawreport):
    report = rawreport[37:53]

    api_key = Key().wclApiKey()

    genReport = ("https://www.warcraftlogs.com:443/v1/report/fights/" + report + "?translate=true&api_key=" + api_key)

    r = requests.get(genReport)
    data = r.json()

    fightID = list()
    bossName = list()
    fightInfo = list()

    fights = data["fights"]


    for f in fights:
        if 'kill' in f and f['kill']:
            fightID.append(f["boss"])
            bossName.append(f['name'])
            if f['difficulty'] == 3:
                fightInfo.append('```Name: ' + f['name'] + ' - Fight ID:' + str(f['boss']) + '-' + str(f["id"]) + ' - Difficulty: Normal```')
            if f['difficulty'] == 4:
                fightInfo.append('```Name: ' + f['name'] + ' - Fight ID:' + str(f['boss']) + '-' + str(f["id"]) + ' - Difficulty: Heroic```')
            if f['difficulty'] == 5:
                fightInfo.append('```Name: ' + f['name']  + ' - Fight ID:' + str(f['boss']) + '-' + str(f["id"]) + ' - Difficulty: Mythic```')

    return ('Here is a list of fights in your log:\n'+''.join(fightInfo)
          +'\nTo specify a fight, use the this command:'
          + '```'
          + '!pawn disc log logURL FightID DIfficulty CharName Realm Zone'
          + '```'
          + '\nFor example: ```!pawn disc log tvXHDjFQdzmV3BkT 2092-44 Djriff Sargeras us```')
        

def wclPawnAndNlcString(self,rawreport,fightID,player,realm,zone)
    #Warcraft Logs import
    report = rawreport[37:53]

    #Pull the stats of the given character
    stats = armoryImport(self, player, realm, zone)

    #Format the data from the armory
    intStat = stats[0]
    critStat = stats[1]
    hasteStat = stats[2]
    mastStat = stats[3]
    versStat = stats[4]
    leechStat  stats[5]
    mainHandIlvl = stats[6]
    
    api_key = Key().wclApiKey()

    genReport ("https://www.warcraftlogs.com:443/v1/report/fights/" + report + "?translate=true&api_key=" + api_key)
    r = requests.get(genReport)
    data = r.json()

    fightEncounterID = fightID[:4]
    fightIDNum = fightID[5:]

    
    

    for x in data:
        fights = data["fights"]
        for f in fights:
            if fightEncounterID == f["boss"] and fightIDNum == f["id"]:
                startTime = f["start_time"]
                endTime = f["end_time"]
        friendlies = data["friendlies"]
        for f in friendlies:
            if player in f["name"]:
                playerID = f["id"]



    tableReport = ("https://www.warcraftlogs.com:443/v1/report/tables/healing/"
        + report
        + "?start=" + str(startTime)
        + "&end=" + str(endTime)
        + "&sourceid=" + str(playerID)
        + "&encounter=" + str(fightID)
        + "&api_key=" + api_key)

    tableR = requests(tableReport)
    table = tableR.json()

    entries = table["entries"]

    #setup healing values
    penanceTotal = 0
    penanceOverheal = 0
    penanceRaw = 0
    penanceOhPercent = 0

    pwrTotal = 0
    pwrOverheal = 0
    pwrRaw = 0
    pwrOhPercent = 0

    pwsTotal = 0
    pwsOverheal = 0
    pwsRaw = 0
    pwsOhPercent = 0

    atonementTotal = 0
    atonementOverheal = 0
    atonementRaw = 0
    atonementOhPercent = 0

    leech = 0

    #atonement percent spells
    atonePenanceTotal = 0
    atonePenanceOverheal = 0
    atonePenanceRaw = 0
    atonePenanceOhPercent = 0

    atoneSmiteTotal = 0
    atoneSmiteOverheal = 0
    atoneSmiteRaw = 0
    atoneSmiteOhPercent = 0

    atonePtWTotal = 0
    atonePtWOverheal = 0
    atonePtWRaw = 0
    atonePtWOhPercent = 0

    atoneSwPTotal = 0
    atoneSwPOverheal = 0
    atoneSwPRaw = 0
    atoneSwPOhPercent = 0


    for e in entries:
        name = e["name"]
        if "Power Word: Radiance" in name:
            pwrTotal += e["total"]
            pwrOverheal += e["overheal"]
            pwrRaw += pwrTotal + pwrOverheal
            pwrOhPercent += pwrOverheal / pwrRaw
        if "Penance" in name:
            penanceTotal += e["total"]
            penanceOverheal += e["overheal"]
            penanceRaw += penanceTotal + penanceOverheal
            penanceOhPercent += penanceOverheal / penanceRaw
        if "Power Word: Shield" in name:
            pwsTotal += e["total"]
            pwsOverheal += e["overheal"]
            pwsRaw += pwsTotal + pwsOverheal
            pwsOhPercent += pwsOverheal / pwsRaw
        if "Atonement" in name:
            atonementTotal += e["total"]
            atonementOverheal += e["overheal"]
            atonementRaw += atonementTotal + atonementOverheal
            atonementOhPercent += atonementOverheal / atonementRaw
            subentries = e["subentries"]
            for a in subentries:
                atoneName = a["name"]
                if "Penance" in atoneName:
                    atonePenanceTotal += a["total"]
                    atonePenanceOverheal += a["overheal"]
                    atonePenanceRaw += atonePenanceTotal + atonePenanceOverheal
                    atonePenanceOhPercent += atonePenanceOverheal / atonePenanceRaw
                if "Smite" in atoneName:
                    atoneSmiteTotal += a["total"]
                    atoneSmiteOverheal += a["overheal"]
                    atoneSmiteRaw += atoneSmiteTotal + atoneSmiteOverheal
                    atoneSmiteOhPercent += atoneSmiteOverheal / atoneSmiteRaw
                if "Purge the Wicked" in atoneName:
                    atonePtWTotal += a["total"]
                    atonePtWOverheal += a["overheal"]
                    atonePtWRaw += atonePtWTotal + atonePtWOverheal
                    atonePtWOhPercent += atonePtWOverheal / atonePtWRaw
                if "Shadow Word: Pain" in atoneName:
                    atoneSwPTotal += a["total"]
                    atoneSwPOverheal += a["overheal"]
                    atoneSwPRaw += atoneSwPTotal + atoneSwPOverheal
                    atoneSwPOhPercent += atoneSwPOverheal / atoneSwPRaw

    #Setup raw healing total
    totalHealing = (pwrRaw + penanceRaw + pwsRaw + atonementRaw)
    totalOverhealingPercent = (pwrOverheal + penanceOverheal + pwsOverheal + atonementOverheal) / totalHealing

    #Find 1% of all healing and use it to calculate how much of each stat we need
    #to get 1% more healing
    totalHealingForOnePercent = totalHealing*0.01
    amountVersNeeded = (totalHealingForOnePercent/totalHealing) * 100 * 475
    amountCritNeeded = (totalHealingForOnePercent/totalHealing) * 100 * 400
    amountMasteryNeeded = (totalHealingForOnePercent/atonementRaw) * 100 * 250
    #Taken from the armory
    amountIntNeeded = intStat/100

    #Set up pawn values from logs and calculate haste weight from it as well.
    pawnInt = 1.00
    pawnVers = amountIntNeeded/amountVersNeeded
    pawnCrit = amountIntNeeded/amountCritNeeded
    pawnMastery = amountIntNeeded/amountMasteryNeeded
    pawnHaste = round(max(pawnCrit,pawnMastery,pawnVers)*1.25/(1+(hasteStat/375/100)),2)
    pawnLeech = round(10000/460/(1+(leechStat/230/100)),2)

    #Pawn String
    pawnString = ('Pawn String: ```( Pawn: v1: "Disc Sheet": Class=Priest, Spec=Discipline,'
                 + 'Intellect=' + str(pawnInt)
                 + ',Leech= ' + str(pawnLeech)
                 + ',HasteRating= ' + str(pawnHaste)
                 + ',MasteryRating= ' + str(pawnMastery)
                 + ',Versatility= ' + str(pawnVers)
                 + ',CritRating= ' + str(pawnCrit)
                 +  ')```' )

    #----------------------------------------------------------------------------------
    #NLC data

    #Pull buff report for Concoordance Uptime
    buffReport = ("https://www.warcraftlogs.com:443/v1/report/tables/buffs/"
                  + report
                  + "?start=" + str(startTime)
                  + "&end=" + str(endTime)
                  + '&by=source'
                  + "&sourceid=" + str(playerID)
                  + "&encounter=" + str(fightID)
                  + "&api_key=" + api_key)



    buffR = requests(buffReport)
    buffs = buffR.json()

    auras = buffs['auras']

    #Average Concoordance Uptime
    concUptime = 0

    for a in auras:
        name = a['name']
        if "Concordance of the Legionfall" in name:
            concUptime = a["totalUptime"]/(endTime-startTime)

    #Disc damage reduction for NLC traits
    dmgReduc = 0.45

    #Haste Percent
    hastePercent = hasteStat/475/100

    #Use a 951 Artifact Weapon as a reference
    referenceInt = 22531
    referenceHaste = 1001
    referenceMast = 1001

    intDiff = round((referenceInt * (pow(1.15,((mainHandIlvl-951)/15)))))
    hasteDiff = round(referenceHaste * (pow(1.15, (mainHandIlvl-951)/15) * pow(0.994435486,(mainHandIlvl-951))))
    mastDiff = calcHaste


    #Atonement Healing Percent
    atonementHealPercent = atonementRaw/totalHealing

    #Setup PP values for +1 to artifact and NLC Traits
    plusOne = round(intDiff * pawnInt + hasteDiff * pawnHaste + mastDiff * pawnMastery,2)
    masterOfShadows = round(500 * pawnMastery)
    lightSpeed = round(500 * pawnHaste)
    chaoticDarkness = round(180000 * (2 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    infusionOfLight = round(101000 * (4 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    shadowBind = round(200000 * (2 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    tormentTheWeak = round(80000 * 4 * dmgReduc * atonementHealPercent,2)
    secureInTheLight = round(135000 * (3 * (1 + hastePercent) / 2) * dmgReduc * atonementHealPercent,2)
    darkSorrows = round(127066 * (1 * (1 + hastePercent)) * dmgReduc * atonementHealPercent,2)
    murderousIntent = round(1500 * concUptime * pawnVers,2)
    shockLight = round(1500 * concUptime * pawnCrit,2)
    refractiveShell = round(300000 * (2 * (1 + hastePercent)) / 60 / 20,2)
    lightsEmbrace = round(45500 * 8 / 60 / 20,2)

    #Generate the Value of each relic
    roundplusOneValue = 1
    masterOfShadows /= plusOne
    lightSpeed /= plusOne
    chaoticDarkness /= plusOne
    infusionOfLight /= plusOne
    shadowBind /= plusOne
    tormentTheWeak /= plusOne
    secureInTheLight /= plusOne
    darkSorrows /= plusOne
    murderousIntent /= plusOne
    shockLight /= plusOne
    refractiveShell /= plusOne
    lightsEmbrace /= plusOne

    #Round everything to 2 decimal points
    roundplusOneValue = round(lightsEmbrace,2)
    masterOfShadows = round(masterOfShadows,2)
    lightSpeed = round(lightSpeed,2)
    chaoticDarkness = round(chaoticDarkness,2)
    infusionOfLight = round(infusionOfLight,2)
    shadowBind = round(shadowBind,2)
    tormentTheWeak = round(tormentTheWeak,2)
    secureInTheLight = round(secureInTheLight,2)
    darkSorrows = round(darkSorrows,2)
    murderousIntent = round(murderousIntent,2)
    shockLight = round(shockLight,2)
    refractiveShell = round(refractiveShell,2)
    lightsEmbrace = round(lightsEmbrace,2)

    #Percent of healing values from Various Logs
    penance = atonePenanceRaw / totalHealing
    pws = pwsRaw / totalHealing
    edge = atonePtWRaw / totalHealing
    bol = pwrRaw / totalHealing
    lr = 0

    #Special Handling for Lenience's Reward

    #Damage Taken
    dmgTakentReport = ("https://www.warcraftlogs.com:443/v1/report/tables/damage-taken/"
                  + report
                  + "?start=" + str(startTime)
                  + "&end=" + str(endTime)
                  + '&by=source'
                  + "&encounter=" + str(fightID)
                  + "&api_key=" + api_key)



    dmgTakenR = requests(dmgTakentReport)
    dmgTaken = dmgTakenR.json()

    entriesDmgTaken = dmgTaken['entries']

    #Set initial value for Damage Taken
    dmgTakenTotal = 0
    raidCnt = 0

    #Loop through the log to find the total damage taken by the raid
    #This also gets a total count of raid members.
    for e in entriesDmgTaken:
        total = e['total']
        dmgTakenTotal += total
        raidCnt += 1

    #Since it's impossible to pull NLC traits for T3, we have to use a baseline of 4 LR traits. Hopefully a workaround
    #can be found in the future
    lr = round(((dmgTakenTotal/(endTime - startTime)) / raidCnt) / (totalHealing/(endTime - startTime)) * 100 / 4,2)

    #NLC String
    nlcString = ('Crucible Weights String: ```cruweight^128868^'
             '197716^' + str(burstOfLight) + '^'
             '252191^' + str(murderousIntent) + '^'
             '238063^' + str(leniencesReward) +  '^'
             '216212^0^'
             '252207^' + str(refractiveShell) + '^'
             '197713^0^'
             '252091^' + str(masterOfShadows) + '^'
             '197729^' + str(shieldOfFaith) + '^'
             '253111^' + str(lightsEmbrace) + '^'
             '252875^' + str(shadowBind) + '^'
             'ilvl^1.00^'
             '197727^^'
             '197711^0^'
             '252922^' + str(darkSorrows) + '^'
             '197715^' + str(edgeOfDarkAndLight) +  '^'
             '252088^' + str(lightSpeed) + '^'
             '252906^' + str(tormentTheWeak) + '^'
             '253093^' + str(infusionOfLight) + '^'
             '197762^0.01 ^'
             '253070^' + str(secureInTheLight) + '^'
             '252888^' + str(chaoticDarkness) + '^'
             '252799^0^'
             '197708^1^end```'	)

    return (pawnString + '\n' + nlcString)





   

