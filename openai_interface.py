'''
OpenAI Chatbot, Enables a user to communicate with the GPT3 Chatbot in a conver
sational manner.
This is the interface between the chatbot and the program.
Modify messages to clear the messages between AI and user.
Modify init_msg to modify the initial system_prompt.
Author: Kanishka Sahoo
'''
import openai


def invoke_key(key):
    openai.api_key = key


class OpenAIBot:
    def __init__(self, init_msg, username):
        self.messages = []
        self.init_msg = init_msg
        self.messages.append({'role': 'system', 'content': self.init_msg})
        self.username = username

    def get_response(self, prompt):
        """
        Gets the response from the given prompt.
        Args:
            prompt: The user-provided prompt.
        Returns:
            response: The AI-provided response.
        """
        # Send the conversation to the OpenAI API
        self.messages.append({'role': 'user', 'content': str(prompt)})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages
        )
        resp = response['choices'][0]['message']
        self.messages.append(resp)
        return resp['content']
