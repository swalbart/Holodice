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

#-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------#

    # test message for text commands
    if message.content.startswith("/status"):
        output = "Ich bin bereit wenn Ihr es seid, Meister"
    elif message.content.startswith("/help") or message.content.startswith("/hilfe"):
        if message.content.startswith("/helpmaster") or message.content.startswith("/hilfemeister") or message.content.startswith("/helpmeister") or message.content.startswith("/hilfemaster"):
            output = helpMaster()
        else:
            output = helpGeneral()
    elif message.content.startswith("/wiki"):
        output = "Wookieepedia: <https://starwars.fandom.com/wiki/Main_Page>"
        output += "\nJedipedia: <https://jedipedia.fandom.com/wiki/Jedipedia:Hauptseite>"
    elif message.content.startswith("/theme"):
        if message.content.startswith("/themeping"):
            output ="@here we go again:\n"
        output += theme()
    elif message.content.startswith("/tren") or message.content.startswith("/cut"):
        output = seperator(message.content)
    elif message.content.startswith("/pew"):
        output = "404 Alderaan not found"
    elif message.content.startswith("/credits"):
        output = "```Holodice by Tobi-Swali\nhttps://github.com/Tobi-Swali\n\nNo Ewoks were harmed during the production of Holodice\n```"

    elif message.content.startswith("/treffer") or message.content.startswith("/hit"):
        output = "Trefferwürfel: " +roll_hit() + authorID
    elif message.content.startswith("/münz") or message.content.startswith("/coin"):
        output = "50/50: " +roll_coin() + authorID

    elif message.content.startswith("/exit0"):
        await message .channel.send("Holowürfel müde - Holowürfel schlafen")
        exit()
    #if (needAuthorID and (not output.startswith("'"'Das ist nicht der Text den ihr sucht'"' ~Obi-Wan Kenobi"))):
    #    output += authorID

    #-----------------------------DICE---------------------------------DICE---------------------------------DICE---------------------------------DICE---------------------------------#

    # dice-command-calculation
    # inputfilter (/ AND d,w,1-9)
    if ((output == "") and (message.content.startswith("/")) and (len(m)>=2) and ((m[1]=="d") or (m[1]=="w") or (m[1]=="1") or (m[1]=="2") or (m[1]=="3") or (m[1]=="4") or (m[1]=="5") or (m[1]=="6") or (m[1]=="7") or (m[1]=="8") or (m[1]=="9"))):
        amountStr = ""              
        diceStr = ""                
        valueStr = ""               
        amount = 0                  # 'amount' of dice
        dice = 0                    # kind of 'dice'
        value = 0                   # operand 'value'
        dw = "x"
        operand = ""
        m = m[-(len(m)-1):]         # remove 1st char ("/")

        # check for 'amount'
        while ((len(m) != 0) and ((m[0] != "d") and (m[0] != "w") and (m[0] != "+") and (m[0] != "-") and (m[0] != "*") and (m[0] != "/"))):
            if(((m[0] == "0") and (amountStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                amountStr += m[0]
            if (len(m)>1):
                m = m[-(len(m)-1):]
            else:
                m = ""
        # edgecase: no amount
        if amountStr == "":
            amountStr = "1"
        # convert 'amount'
        amount = int(amountStr)

        # if m is still a message go on
        if len(m) !=0:
            if ((m[0] == "d") or (m[0] == "w")):
                dw = m[0]
                m = m[-(len(m)-1):]

            # check 'dice'
            while ((len(m) != 0) and ((m[0] != "+") and (m[0] != "-") and (m[0] != "*") and (m[0] != "/"))):
                if(((m[0] == "0") and (diceStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                    diceStr += m[0]
                if (len(m)>1):
                    m = m[-(len(m)-1):] 
                else:
                    m = "+"
            # convert 'dice'
            if diceStr !="":
                dice = int(diceStr)

            # check 'operand'
            if len(m) >1:
                operand = m[0]
                m= m[-(len(m)-1):]

                # check 'value'
                while (len(m) != 0):
                    if(((m[0] == "0") and (valueStr !="")) or (m[0] == "1") or (m[0] == "2") or (m[0] == "3") or (m[0] == "4") or (m[0] == "5") or (m[0] == "6") or (m[0] == "7") or (m[0] == "8") or (m[0] == "9")):
                        valueStr += m[0]
                    if (len(m)>1):
                        m = m[-(len(m)-1):] 
                    else:
                        m = "" 
                # convert 'value'
                value = int(valueStr)
        
        # short throws (/X)
        if dw == "x":
            # short throw (/1 /2 /3 = 1d20 2d20 3d20)
            if amount <= 3:
                dice =20
                diceStr ="20"
            # short throw (/X =1dX)
            else:
                dice = amount
                diceStr = amountStr
                amount = 1
                amountStr = "1"
            dw = "d"

        # roll the dice
        if  (dice>0):
            if(value>0):
                output = "Rolled: " +amountStr +"x " +dw +diceStr +" " +operand +valueStr +":   " +roll(amount, dice, operand, value) +authorID
            else:
                output = "Rolled: " +amountStr +"x " +dw +diceStr +":   " +roll(amount, dice, operand, value) +authorID
        else:
            output = "Command failed"
            # for debugging
            print(output+": <"+message.content+"> (["+amountStr+";"+str(amount)+"]["+dw+"]["+diceStr+";"+str(dice)+"]["+operand+"]["+valueStr+"]["+str(value)+"])")

    # check if any 'output' available
    if output == "":
        # No 'output' means incorrect command
        output = "'"'Das sind nicht die Befehle die Ihr sucht'"' ~Obi-Wan Kenobi (try '/help')"
    # send the 'output' to discord
    await message.channel.send(output)

#-----------------------------HELP---------------------------------HELP---------------------------------HELP---------------------------------HELP---------------------------------#

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

#-----------------------------METHODS------------------------------METHODS------------------------------METHODS------------------------------METHODS------------------------------#

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

# roll hit body dice
def roll_hit():
    # frequencies of body parts (customizable:)
    # (standard DsA: 3,3,2,2,4)
    arm = 3         # (consider: it's the value per arm)
    leg = 3         # (consider: it's the value per leg)
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
        hit = "Rolling hit body dice failed"
    return hit
    

# flip coin
def roll_coin():
    coin = random.randint(1, 2)
    if coin==1:
        return "Hoch/Kopf"
    elif coin==2:
        return "Tief/Zahl"
    else:
        return "Flip coin failed"

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

#-----------------------------VISUALS------------------------------VISUALS------------------------------VISUALS------------------------------VISUALS------------------------------#

def theme():    #  slightly modified from http://www.ascii-art.de/ascii/s/starwars.txt
    output =  "```.        .          .    .    .            .            .                   .\n"
    output +=    "       .      .               ..       .       .   .             .\n"
    output +=    " .            I n   t h e   l a s t   e p i s o d e   o f   . . .             .\n"
    output +=    "                     .              .       .                      .      .\n"
    output +=    ".       .                .       .     .            .\n"
    output +=    "   .           .        .                     .        .            .\n"
    output +=    "             .               .    .          .              .   .         .\n"
    output +=    "               _________________      ____         __________         .\n"
    output +=    " .       .    /                 |    /    \    .  |          \ \n"
    output +=    "    .        /    ______   _____| . /      \      |    ___    |     .     .\n"
    output +=    "             \    \    |   |       /   /\   \     |   |___>   |\n"
    output +=    "           .  \    \   |   |      /   /__\   \  . |         _/               .\n"
    output +=    " .     ________>    |  |   | .   /            \   |   |\    \_______    .\n"
    output +=    "      |            /   |   |    /    ______    \  |   | \           |\n"
    output +=    "      |___________/    |___|   /____/      \____\ |___|  \__________|    .\n"
    output +=    "  .     ____    __  . _____   ____      .  __________   .  _________\n"
    output +=    "       \    \  /  \  /    /  /    \       |          \    /         |      .\n"
    output +=    "        \    \/    \/    /  /      \      |    ___    |  /    ______|  .\n"
    output +=    "         \              /  /   /\   \ .   |   |___>   |  \    \ \n"
    output +=    "   .      \            /  /   /__\   \    |         _/.   \    \            .\n"
    output +=    "           \    /\    /  /            \   |   |\    \______>    |   .\n"
    output +=    "            \  /  \  /  /    ______    \  |   | \              /          .\n"
    output +=    " .       .   \/    \/  /____/      \____\ |___|  \____________/     \n"
    output +=    "                  .            .                                        .\n"
    output +=    "     .                           .         .               .                 .\n"
    output +=    "                .            .                      .            .\n```"
    return output

#-----------------------------TOKEN--------------------------------TOKEN--------------------------------TOKEN--------------------------------TOKEN--------------------------------#

#-------------------------------------------------------------------------------------------------------------------------#
# For all who rather want to paste the token here instead of saveing it to the token.txt can do it the following way.     #
# But I reccomend to not keep in the sourcecode because the key is unique and anyone can controll your bot with this key: #
#-------------------------------------------------------------------------------------------------------------------------#
token = "mytoken" # replace the word <mytoken> with your 59 character token

if(len(token)<59):
    # check for token in token.txt
    token_path = 'token.txt'
    if os.path.exists(token_path):
        # token exits in token.txt
        with open(token_path, 'r') as file:
            token = file.read().replace('\n', '') 
    else:
        # no token found
        print("\nFor your Information:")
        print("To protect your token from beeing detected in the sourcecode of holodice it will get stored in a seperate file named token.txt in the same folder.")
        print("You can find the token in the bot-configuration of the discord developers portal.")
        print("This is a one-time process, so next time you start the bot it will be able to get the token automaticly from the token.txt.\n")
        token = input("Discord token:")
        with open(token_path, 'w') as file:
            file.write(token)
client.run(token)