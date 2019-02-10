import logging
import os
from chessboard import *
from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

commands = None
main = main()


@ask.launch
def launch():
    speechtext = "White's move"
    return question(speechText).reprompt(speechText).simple_card(speechText)

@ask.intent('movePiece')
def parseInput(position_One, position_Two):
    commandsBegin = position_One.split(' ')
    commandsEnd = position_Two.split(' ')
        
    commands = [commandsBegin[0], commandsBegin[1], commandsEnd[0], commandsEnd[1]]
    print(commands)
    main.parseCommand(commands)
    return commands
    
@ask.session_ended
def sessionEnded():
    return "{}", 200

if __name__ == '__main__':
    app.run(debug=True)
            