'''
OpenAI Chatbot, Enables a user to communicate with the GPT3 Chatbot in a conver
sational manner.
This is the interface between the chatbot and the program.
Modify messages to clear the messages between AI and user.
Modify init_msg to modify the initial system_prompt.
Author: Kanishka Sahoo
'''
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the OpenAI API key, loaded from a .env file containing the token as AP
# I_TOKEN=""
openai.api_key = str(os.environ["API_TOKEN"])

messages = []
use_model = 'gpt-3.5-turbo'
init_msg = ''


def get_response(prompt):
    """
    Gets the response from the given prompt.
    Args:
        prompt: The user-provided prompt.
    Returns:
        response: The AI-provided response.
    """
    global messages
    # Send the conversation to the OpenAI API
    messages.append({'role': 'system', 'content': init_msg})
    messages.append({'role': 'user', 'content': str(prompt)})
    response = openai.ChatCompletion.create(
        model=use_model,
        messages=messages
    )
    resp = response['choices'][0]['message']
    messages.append(resp)
    return resp['content']
