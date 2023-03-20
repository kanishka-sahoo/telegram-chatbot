#!/usr/bin/python3
import openai_interface as oif


def main():
    # opening_prompt = input("Enter opening prompt: ")
    # variable to keep track of the conversation.
    model = 'gpt-3.5-turbo'
    oif.use_model = model
    user_input = input("--> ")
    while user_input:
        resp = oif.get_response(user_input)
        print(resp)
        user_input = input("--> ")


if __name__ == "__main__":
    main()
