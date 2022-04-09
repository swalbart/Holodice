# Changelog

## 0.3.3 - Information update
* ### Information update
    * Added Changelog.md
    * Reworked README.md

## 0.3.2 - Language update
* ### Language update
    * Added english xml file (en.xml)
    * Added german xml file (de.xml)
    * Replaced static (hardcoded) outputs with getable lines of language xml files
    * Selected english as default Language (The bot will start in default language)
    * Added language command to help
* ### Other
    * Typo correction
    * Removed unneccessary imports
    * Fixed 'd1, d2 and d3' to not output '1d20, 2d20 and 3d20'
    * Updated credits information

## 0.3.1 - Dice rework update
* ### Dice rework update
    * Reworked dice command calculation
    * Removed quickfix for /X commands
* ### Other
    * Added '/version' command
    * Added dividers between code sections
    * Added text to README.md
    * Edited help texts
    * Edited messages for failed commands
    * Edited '/cut' output

## 0.3.0 - Token update
* ### Token update
    * Added .gitignore
    * Removed Token from Holodice.py
    * Added code to store the bot token in a token.txt
    * Added token chapter in .gitignore to prevent an upload of a token
    * Added code to check if a token is existing, else it asks for it and stores it
* ### Other
    * Started hosting the Code on github

## 0.2.2 - Feedback update
* ### Feedback update
    * Added output texts for all possible '/' commands
    * Added output text to show exactly what the bot calculated in form of "Rolled: ... : ..."
    * Added author tag to every dice command to identify multiple input command outputs
* ### Other
    * Quickfixed not working '/X commands'

## 0.2.1 - Operation update
* ### Operation update
    * Added operations with four different operands to be captured by the code

## 0.2.0 - Dynamic Dice update
* ### Dynamic Dice update
    * Removed static (hardcoded) dice check commands
    * Added algorithm to check dice dynamicly by discord chat comand input

## 0.1.2 - Creator update
* ### Creator update
    * Added '/credits' command to link the origin-repository
* ### Other
    * Added '/theme' and '/themeping' as commented out commands for ascii art to be inserted there

## 0.1.1 - Command update
* ### Command update
    * Added '/wiki' command to get links to the wiki-webpages
    * Added '/cut' command

## 0.1.0 - Hit and flip update
* ### Hit and flip update
    * Added hit dice to determine hit body part
    * Added coin flip as alternative to 'd2'

## 0.0.3 - Shutdown update
* ### Shutdown update
    * Added '/exit0' command to shut down the bot manually with a discord command

## 0.0.2 - Dice update
* ### Dice update
    * Added randomizer
    * Added common dice (d4, d6, d8, d10, d12, d20)
    * Added more dice (d2, d24, d100, d1000)
* ### Edits
    * Replaced '/hello' with '/status'-ping

## 0.0.1 - Hello world
* ### Hello world
    * Added '/hello' command