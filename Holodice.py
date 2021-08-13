import discord
import random
import time
import os
import subprocess
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

@client.event
async def on_message(message):
    # make sure to not get triggered by own messages
    if message.author == client.user:
        return
    message.content =message.content.lower()
    m= message.content
    output = ""
    authorID = " <@" +str(message.author.id) +">"

    # test for text commands
    if message.content.startswith("/status"):
        output = "Ich bin bereit wenn Ihr es seid, Meister"
    elif message.content.startswith("/help") or message.content.startswith("/hilfe"):
        if message.content.startswith("/helpmaster") or message.content.startswith("/hilfemeister") or message.content.startswith("/helpmeister") or message.content.startswith("/hilfemaster"):
            output = helpMaster()
        else:
            output = helpGeneral()
    elif message.content.startswith("/wiki"):
        output = "Wookieepedia: <https://starwars.fandom.com/wiki/Main_Page> \nJedipedia: <https://jedipedia.fandom.com/wiki/Jedipedia:Hauptseite>"
    elif message.content.startswith("/theme"):
        if message.content.startswith("/themeping"):
            output ="@here we go again:\n"
        output += "```.        .          .    .    .            .            .                   .\n               .               ..       .       .   .             .\n .      .     I n   t h e   l a s t   e p i s o d e   o f   . . .             .\n                     .              .       .                    .      .\n.        .               .       .     .            .\n   .           .        .                     .        .            .\n             .               .    .          .              .   .         .\n               _________________      ____         __________\n .       .    /                 |    /    \    .  |          \ \n     .       /    ______   _____| . /      \      |    ___    |     .     .\n             \    \    |   |       /   /\   \     |   |___>   |\n           .  \    \   |   |      /   /__\   \  . |         _/               .\n .     ________>    |  |   | .   /            \   |   |\    \_______    .\n      |            /   |   |    /    ______    \  |   | \           |\n      |___________/    |___|   /____/      \____\ |___|  \__________|    .\n  .     ____    __  . _____   ____      .  __________   .  _________\n       \    \  /  \  /    /  /    \       |          \    /         |      .\n        \    \/    \/    /  /      \      |    ___    |  /    ______|  .\n         \              /  /   /\   \ .   |   |___>   |  \    \ \n   .      \            /  /   /__\   \    |         _/.   \    \            +\n           \    /\    /  /            \   |   |\    \______>    |   .\n            \  /  \  /  /    ______    \  |   | \              /          .\n .       .   \/    \/  /____/      \____\ |___|  \____________/  DSA\n                               .                                        .\n     .                           .         .               .                 .\n                .                                   .            .\n```"
    elif message.content.startswith("/tren") or message.content.startswith("/cut"):
        output = seperator(message.content)
    elif message.content.startswith("/pew"):
        output = "404 Alderaan not found"
    elif message.content.startswith("/credits"):
        output = "```Holodice by Tarees\nunter beobachtung von Lordi\n\nNo Ewoks were harmed during the production of Holodice\n(Ich werde hier wirklich überhaupt gar nicht von\n einem Sith Lord gezwungen das dazu zu schreiben.)\n\n$3(\)D |-|3£P \n              -74R335```"

    elif message.content.startswith("/treffer") or message.content.startswith("/hit"):
        output = "Trefferwürfel: " +roll_hit() + authorID
    elif message.content.startswith("/münz") or message.content.startswith("/coin"):
        output = "50/50: " +roll_coin() + authorID

    elif message.content.startswith("/exit0"):
        await message .channel.send("Holowürfel müde - Holowürfel schlafen")
        exit()
    #if (needAuthorID and (not output.startswith("'"'Das ist nicht der Text den ihr sucht'"' ~Tobi-Wan Kenobi"))):
    #    output += authorID

    #quickfix for /X commands
    if (m=="/1"):
        m="/1w20"
    elif (m=="/2"):
        m="/2w20"
    elif (m=="/3"):
        m="/3w20"
    elif (m=="/4"):
        m="/1w4"
    elif (m=="/5"):
        m="/1w5"
    elif (m=="/6"):
        m="/1w6"
    elif (m=="/7"):
        m="/1w7"
    elif (m=="/8"):
        m="/1w8"
    elif (m=="/9"):
        m="/1w9"

    # dice-command-calculation
    # only if output is empty, message is a slash-command AND first char after '/' is allowed
    if ((output == "") and (message.content.startswith("/")) and (len(m)>2) and ((m[1]=="d") or (m[1]=="w") or (m[1]=="0") or (m[1]=="1") or (m[1]=="2") or (m[1]=="3") or (m[1]=="4") or (m[1]=="5") or (m[1]=="6") or (m[1]=="7") or (m[1]=="8") or (m[1]=="9"))):
        amountStr = ""
        diceStr = ""
        valueStr = ""
        amount = 1
        dice = 0
        value = 0       # value for the calculation with the operator
        dw = "x"
        operator = ""
        # remove the "/" from the input message (message.content)
        # l = length of string m; m = message
        m = m[-(len(m)-1):]
        # check command for amount (and shorten message-string) [while not next command, do...]
        while ((len(m) != 0) and ((m[0] != "d") and (m[0] != "w") and (m[0] != "+") and (m[0] != "-") and (m[0] != "*") and (m[0] != "/"))):
            if(((m[0] == "0") and (amountStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                amountStr += m[0]
            if (len(m)>1):
                m = m[-(len(m)-1):] 
            else:
                m = ""
        # if no amount occur use one dice
        if amountStr == "":
            amountStr = "1" # amount is already initializes with 1
        # convert amount
        amount = int(amountStr)
        # if m is still a message go on
        if len(m) !=0:
            if ((m[0] == "d") or (m[0] == "w")):
                # rewrite dw (and shorten message-string)
                dw = m[0]
                m = m[-(len(m)-1):]
            # check command for number (and shorten message-string) [while not next command, do...] ------------------------------
            while ((len(m) != 0) and ((m[0] != "+") and (m[0] != "-") and (m[0] != "*") and (m[0] != "/"))):
                if(((m[0] == "0") and (diceStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                    diceStr += m[0]
                    print
                if (len(m)>1):
                    m = m[-(len(m)-1):] 
                else:
                    m = "+"
            # some commands have no dice in this position. (/4+2 here the dice is in first place)
            if diceStr !="":
                dice = int(diceStr)
            # continue only if amount is a number (cant roll a 0-sided dice)
            if len(m) >1:
                # check command for operation (+-*/)
                operator = m[0]
                m= m[-(len(m)-1):]
                # check command for value
                while (len(m) != 0):
                    if(((m[0] == "0") and (valueStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                        valueStr += m[0]
                    if (len(m)>1):
                        m = m[-(len(m)-1):] 
                    else:
                        m = "" 
                    #m = m[-(len(m)-1):]
                value = int(valueStr)
        if dw == "x":
            # commands with only one number (z.B. /6) have the dice in first place instead of the amount
            if amount <= 3:
                # special case: /1 /2 /3 are equal to /1w20 /2w20 /3w20
                dice =20
                diceStr ="20"
            else:
                dice = amount
                diceStr = amountStr
                amount = 1
                amountStr = "1"
            dw = "d"
        # roll the dice
        if  (dice>0):
            output = "Rolled: " +amountStr +"x " +dw +diceStr +":   " +roll(amount, dice, operator, value) +authorID
        else:
            output = ""

    if output == "":
        output = "'"'Das sind nicht die Befehle die Ihr sucht'"' ~Tobi-Wan Kenobi (try '/help')"
    await message.channel.send(output)

def helpGeneral():
    m = "```" # 3 characters (helpMaster())
    output0 = "**Viel zu lernen du noch hast:**\n" # 34 characters (helpMaster())
    output1 = "Vereinfachte 20er: /1 /2 /3      | / & menge an 20ern [max.3]\n"
    output2 = "Einfache Würfe:    /10 /6+2      | / & würfel [ab 4] & (+-*/ & Wert)\n"
    output3 = "Eingabe:           /2d6+5        | / & (Menge) & d|w & Würfel & (+-*/ & Wert)\n" 
    output4 = "Münzwurf (50/50):  /coin /münze  | Liefert genau: Hoch/Kopf bzw. Tief/Zahl\n"
    output5 = "Trefferwürfel:     /hit /treffer | Gibt Trefferzone an\n"
    output6 = "Links:             /wiki         | Wookieepedia und Jedipedia\n"
    output7 = "Credits:           /credits      | Holodice Credits"
    return (output0 +m +output1 +output2 +output3 +output4 +output5 +output6 +output7 +m)

def helpMaster():
    m = "```"
    output0 = "**Hier mein Lord, wie Ihr befahlt:**\n"
    output1 = "Status:            /status       | gibt bescheid ob Bot bereit ist\n"
    output2 = "Theme:             /theme        | gibt aus: In the last episode of... + Bild\n"
    output3 = "                   /themeping    | wie theme, pingt aber alle\n"
    output4 = "Trennlinie:        /trenner Text | trenn.../cut + Trennlinientext\n"
    output5 = "                                 | Alles nach dem ersten Leerzeichen wird Trennlinientext\n"
    output6 = "Bot ausschalten:   /exit0        | ACHTUNG: Bot startet nicht automatisch neu\n\n"
    outputHelp =(helpGeneral())
    # cut of the first 37 charactersof outputHelp
    outputHelp = outputHelp[-(len(outputHelp)-36):]
    return (output0 +m +output1 +output2 +output3 +output4 +output5 +output6 +outputHelp)




# seperator line with custom text
def seperator(m):
    output1 = "```|\n|~==+++<<<<#####$$$$$$§§§§§§§"
    output2 = " §§§§§§§$$$$$$#####>>>>+++==~\n| ```"
    messageArr = m.split()
    messageArgs = len(messageArr)
    argsCounter = 1
    message = ""
    while argsCounter<messageArgs:
        message += (" " +messageArr[argsCounter])
        argsCounter += 1
    return (output1 +message +output2)

# roll hit dice
def roll_hit():
    # frequencies of body parts (customizable:)
    # (standard DsA: 3,3,2,2,4)
    arm = 3
    leg = 3
    head = 2
    stomach = 2
    torso = 4
    # sum up and roll dice
    amount = (2*arm +2*leg +head +stomach +torso)
    result = random.randint(1, amount)
    hit = ""
    if result<=arm:
        hit = "Linker Arm"
    elif result<=(2*arm):
        hit = "Rechter Arm"
    elif result<=(2*arm +leg):
        hit = "Linkes Bein"
    elif result<=(2*(arm+leg)):
        hit = "Rechtes Bein"
    elif result<=(amount-(stomach +torso)):
        hit = "Kopf"
    elif result<=(amount-torso):
        hit = "Rücken"
    elif result<=amount:
        hit = "Brust"
    else:
        hit = "404 Alderaan not found"
    return hit
    

# flip coin
def roll_coin():
    coin = random.randint(1, 2)
    if coin==1:
        return "Hoch/Kopf"
    elif coin==2:
        return "Tief/Zahl"
    else:
        return "404 Alderaan not found"

# roll dice
# a = amount; d = dice-sides; o = operator; v = value for operator
def roll(a, d, o, v):
    # roll the dice and sum up to total
    num = random.randint(1, d)
    total = num
    output = str(total)
    counter = a
    while counter>1:
        num = random.randint(1, d)
        total += num
        output += (" + " +str(num))
        counter -= 1
    if a != 1:
        output += (" = " +str(total))
    # calculate with operator if given
    if o != "":
        output += (" " +o +" " +str(v) +" = ")
        if o == "+":
            output += str(total+v)
        elif o == "-":
            output += str(total-v)
        elif o == "*":
            output += str(total*v)
        elif o == "/":
            output += (str(round((total/v),2))+"*")
    return output

token_path = 'token.txt'

if os.path.exists(token_path):
    with open(token_path, 'r') as file:
        token = file.read().replace('\n', '')
else:
    token = input("Discord Token:")
    with open(token_path, 'w') as file:
        file.write(token)


# do not keep the key below for public. The key is unique and anyone can controll your bot with this key:
client.run(token)