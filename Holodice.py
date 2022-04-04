from re import I
import discord
import random
import os
import python_lang as lang

client = discord.Client()
lang.add("languages/en.xml", "english")
lang.add("languages/de.xml", "deutsch")
#lang.add("languages/test.xml", "test")  # for language tests
lang.select("en")
print("Greetings, The bot boots with its default language: "+lang.selected+".")

# useful shortcut and markdown as variables for coding
rt = "\n"       # rt = return
cb = "```"      # cb = codeblock
ii = "*"        # ii = italics
bb = "**"       # bb = bold
ib = "***"      # ib = italics and bold
uu = "__"       # uu = underlined
cc = "~~"       # cc = crossed (out)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

@client.event
async def on_message(message):
    # make sure to not get triggered by own messages
    if message.author == client.user:
        return
    m = message.content
    m = m.lower()
    
    output = ""
    authorID = " <@" +str(message.author.id) +">"

#-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------COMMANDS-----------------------------#

    if m.startswith(getLine("cmd")) or m.startswith(getLineDefault("cmd")):
        m = m[-(len(m)-1):]                 # remove first charater
        # test message for text commands
        if m.startswith(getLine("cmd_status")) or m.startswith(getLineDefault("cmd_status")):
                output = getLine("status")
        elif m.startswith(getLine("cmd_help_player")) or m.startswith(getLineDefault("cmd_help_player")):
            output = cb
            if m.startswith(getLine("cmd_help_master1")) or m.startswith(getLine("cmd_help_master2")) or m.startswith(getLineDefault("cmd_help_master1")) or m.startswith(getLineDefault("cmd_help_master2")):
                output += getLine("help_master01")+rt+getLine("help_master02")+rt+getLine("help_master03")+rt+getLine("help_master04")+rt+getLine("help_master05")+rt+getLine("help_master06")+rt+getLine("help_master07")+rt+getLine("help_master08")+rt+getLine("help_master09")+rt+rt
            output += getLine("help_player01")+rt+getLine("help_player02")+rt+getLine("help_player03")+rt+getLine("help_player04")+rt+getLine("help_player05")+rt+getLine("help_player06")+rt+getLine("help_player07")+cb
        elif m.startswith(getLine("cmd_links")) or m.startswith(getLineDefault("cmd_links")):
            output = getLine("links1")+rt+getLine("links2")
        elif m.startswith(getLine("cmd_theme")):
            if m.startswith(getLine("cmd_themeping")):
                output = getLine("themeping")+rt
            output += theme()
        elif m.startswith(getLine("cmd_cut")) or m.startswith(getLineDefault("cmd_cut")):
            output = seperator(m)
        elif m.startswith("alder"):
            output = "404 Alderaan not found"
        elif m.startswith("/pew") or m.startswith("pew"):
            output= ii+"miss"+ii
            if m.startswith("/pewpew") or m.startswith("/pew pew") or m.startswith("pewpew") or m.startswith("pew pew"):
                output= bb+"miss intensifies"+bb
                if m.startswith("/pewpewpew") or m.startswith("/pew pew pew") or m.startswith("pewpewpew") or m.startswith("pew pew pew"):
                    output = ib+"critical miss"+ib
                    if m.startswith("/pewpewpewpew") or m.startswith("/pew pew pew pew") or m.startswith("pewpewpewpew") or m.startswith("pew pew pew pew"):
                        output = "Lets be "+ii+"realistic"+ii+", as a "+bb+"Stormtrooper"+bb+" you would be "+ib+"dead after three missed chances"+ib
        elif m.startswith(getLine("cmd_credits")) or m.startswith(getLineDefault("cmd_credits")):
            output = getLine("credits1")+rt+getLine("credits2")+rt+getLine("credits3")+rt+getLine("credits4")
        elif m.startswith(getLine("cmd_hit")) or m.startswith(getLineDefault("cmd_hit")):
            output = getLine("hit") +roll_hit() + authorID
        elif m.startswith(getLine("cmd_coin")) or m.startswith(getLineDefault("cmd_coin")):
            output = getLine("coin") +roll_coin() + authorID
        # languages
        elif m.startswith(getLine("cmd_language")) or m.startswith(getLineDefault("cmd_language")):
            output = language(m)
        # maintenance
        elif m.startswith(getLine("cmd_shutdown")) or m.startswith(getLineDefault("cmd_shutdown")):
            await message.channel.send(getLine("shutdown"))
            exit()
        elif m.startswith("dev"):   # unlisted in xml-language-files
            output = getLine("status")
        elif m.startswith(getLine("cmd_version")) or m.startswith(getLineDefault("cmd_version")):
            output = "0.3.2"

    #-----------------------------DICE---------------------------------DICE---------------------------------DICE---------------------------------DICE---------------------------------#

        # dice-command-calculation
        # inputfilter (d,w,1-9)
        if (output == "" and (len(m)>=1) and ((m[0]=="d") or (m[0]=="w") or (m[0]=="1") or (m[0]=="2") or (m[0]=="3") or (m[0]=="4") or (m[0]=="5") or (m[0]=="6") or (m[0]=="7") or (m[0]=="8") or (m[0]=="9"))):
            amountStr = ""              
            diceStr = ""                
            valueStr = ""               
            amount = 0                  # 'amount' of dice
            dice = 0                    # kind of 'dice'
            value = 0                   # operand 'value'
            dw = "x"
            operand = ""                # 'operand'

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
                print(output+": <"+m+"> (["+amountStr+";"+str(amount)+"]["+dw+"]["+diceStr+";"+str(dice)+"]["+operand+"]["+valueStr+"]["+str(value)+"])")

        # check if any 'output' available
        if output == "":
            # No 'output' means incorrect command
            output = getLine("general_error_input")
        # send the 'output' to discord
        await message.channel.send(output)

#-----------------------------LANGUAGE-----------------------------LANGUAGE-----------------------------LANGUAGE-----------------------------LANGUAGE-----------------------------#

def getLanguages():         # get all available languages
    return lang.all()

def getLine(text):          # line=keyword to output-string in xml
    return getLineSuper(text, False)

def getLineDefault(text):
    return getLineSuper(text, True)

def getLineSuper(text, defaultLanguage):            # line=keyword to output-string in xml
    if defaultLanguage:
        temp = lang.selected
        lang.select("en")
    output = ""
    output = lang.get(text)                         # set output to deposited string of the ordered 'text'-command in the currently chosen language
    if output == text:                              # recursive check (if text of current language equals text of this method call)
        if not defaultLanguage:
            output = getLineDefault(text)
        else:
            output = "Error: Getting language text failed [for: "+text+"] (∿•͟ ͜ •)∿ ︵ ┻━┻"
        if output.startswith("Error"):
            output += rt+"Redirected to english. Could not find "+text+" in "+str(lang.selected)+" language"
    output = output.lstrip(" ")                     # erase leading whitespaces from xml files
    if output.startswith("."):                      # replace first '.' with a whitespace
        output = output[-(len(output)-1):]
        output = " "+output
    if defaultLanguage:
        lang.select(str(temp))
    return output
    
def language(m):
    output = ""
    mArray = m.split()
    printLangInfo = True
    if len(mArray) == 2:                                    # allwos two arguments (2nd arguement is language string)
        for element in getLanguages():
            if (mArray[1] in element) and output == "":     # check if input language string is valid
                lang.select(mArray[1])
                output = getLine("language_change_success")+" "+lang.selected+rt
                printLangInfo = False
        if output == "":                                    # non-valid language: error
            output += getLine("language_error_unknown")+" ("+mArray[1]+")"+rt
    elif len(mArray) > 2:                                   # too many arguments: error
        output += getLine("language_error_too_many_arguments")+rt
    if printLangInfo:                                       # adds info about 'lang' command
        output += getLine("language_selected")+lang.selected+rt
        output += getLine("language_change_text")
        output += " **"+getLine("cmd")+getLine("cmd_language")+" xx**"+rt
        output += getLine("language_replace_text")+str(getLanguages())
    return output

#-----------------------------METHODS------------------------------METHODS------------------------------METHODS------------------------------METHODS------------------------------#

# seperator line with custom text
def seperator(m):
    output1 = "```\\\n |~==+++<<<<#####$$$$$$§§§§§§§"
    output2 = " §§§§§§§$$$$$$#####>>>>+++==~\n/```"
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
    chest = 2
    back = 4
    # sum up and roll dice
    amount = (2*arm +2*leg +head +chest +back)
    result = random.randint(1, amount)
    hit = ""
    if result<=arm:
        hit = getLine("hit_arm_left")
    elif result<=(2*arm):
        hit = getLine("hit_arm_right")
    elif result<=(2*arm +leg):
        hit = getLine("hit_leg_left")
    elif result<=(2*(arm+leg)):
        hit = getLine("hit_leg_right")
    elif result<=(amount-(chest +chest)):
        hit = getLine("hit_head")
    elif result<=(amount-chest):
        hit = getLine("hit_back")
    elif result<=amount:
        hit = getLine("hit_chest")
    else:
        hit = getLine("hit_error")
    return hit
    
# flip coin
def roll_coin():
    coin = random.randint(1, 2)
    output = ""
    if coin==1:
        output = getLine("coin_high")
    elif coin==2:
        output = getLine("coin_low")
    else:
        output = getLine("coin_error")
    return output

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
token = "mytoken" # here you are able to replace the word <mytoken> with your 59 character token (not recommended)

if(len(token)<59):
    # check for token in token.txt
    token_path = 'token.txt'
    if os.path.exists(token_path):
        # token exits in token.txt
        with open(token_path, 'r') as file:
            token = file.read().replace('\n', '') 
    else:
        # no token found
        tokenInit = rt+getLine("token1")+rt+getLine("token2")+rt+getLine("token3")+rt+getLine("token4")
        token = input("Discord token:")
        with open(token_path, 'w') as file:
            file.write(token)
client.run(token)