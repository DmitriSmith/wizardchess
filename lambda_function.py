import json

def lambda_handler(event, context):
    # TODO implement
    
    if (event["session"]["application"]["applicationId"] != "amzn1.ask.skill.87b42952-c1bc-4923-8103-e78e3a61190d"):
        raise ValueError("Invalid Application ID")          
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
        
    
def on_session_started(session_started_request, session):
    print("Starting new session.")

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    
    if intent_name == "startGameOfChess":
        return startGame("Game starting")
    elif intent_name == "movePiece":
        pos1 = intent_request["intent"]["slots"]["position_One"]["value"]
        pos2 = intent_request["intent"]["slots"]["position_Two"]["value"]
        return movePiece(pos1, pos2 , "Moving Piece")
    elif intent_name == "undoMove":
        return undoMove("Undo move")
    
def startGame(text):
    session_attributes = {}
    card_title = text
    reprompt_text = ""
    should_end_session = False

    speech_output = "The game has begun. It is now white's move. Please designate the location of which piece you want to move!"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def movePiece(pos1, pos2, text):
    session_attributes = {}
    card_title = text
    reprompt_text = ""
    should_end_session = False

    speech_output = "moving " + pos1 + ", to " + pos2
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def undoMove(text):
    session_attributes = {}
    card_title = text
    reprompt_text = ""
    should_end_session = False

    speech_output = "Undoing the last move"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_session_ended(session_ended_request, session):
    print("Ending session.")

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
                "type": "PlainText",
                "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }