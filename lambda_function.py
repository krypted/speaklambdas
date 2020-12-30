# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder. This is sample code so
# check everything before putting it into production.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
import boto3
import json

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

skill_name = "My Color Session"
help_text = ("Please tell me your favorite color. You can say "
             "my favorite color is red")

color_slot_key = "COLOR"
color_slot = "Color"

# Define the client to interact with AWS Lambda
client = boto3.client('lambda')


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Lambda function invoking skill. You can say 'can you please start the function walmart?'. Then, i will trigger the function and get a response"

    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("InvokeLambdaIntent"))
def invoke_lambda_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Sorry. Unable to find any child lambda function"
    slots = handler_input.request_envelope.request.intent.slots
    lambdaname = slots['lambdaname'].value.lower()
    logger.info("slots {}".format(slots))    
    logger.info("slots lambdaname {}".format(slots["lambdaname"]))   
    logger.info("slots lambdaname value {}".format(slots["lambdaname"].value))   
    if lambdaname.lower() == "walmart":
        response = client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:xxxxxx:function:walmart',
            InvocationType='RequestResponse'
        )

        responseFromChild = json.load(response['Payload'])
        speech_text = responseFromChild["body"]
    elif lambdaname.lower() == "swiggy":
        response = client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:xxxxx:function:swiggy',
            InvocationType='RequestResponse'
        )
        responseFromChild = json.load(response['Payload'])
        speech_text = responseFromChild["body"]
    elif lambdaname.lower() == "amazon":
        response = client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:xxxxxxxx:function:amazon',
            InvocationType='RequestResponse'
        )
        responseFromChild = json.load(response['Payload'])
        speech_text = responseFromChild["body"]

    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can say 'can you please start the function walmart?'. Then, i will trigger the function and get a response"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Lambda Invoking Skill", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Lambda Invoking Skill", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Lambda Invoking Skill can't help you with that.  "
        "You can say 'can you please start the function walmart?'. Then, i will trigger the function and get a response")
    reprompt = "You can say 'can you please start the function walmart?'. Then, i will trigger the function and get a response"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
