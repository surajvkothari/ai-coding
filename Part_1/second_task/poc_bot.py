from openai import OpenAI


def bot_v2(messages):
    """
    In version 2, the bot remembers what the user has sent so it won't respond with the same list of preferences.
    """
    
    client = OpenAI()

    system_prompt = """You are an assistant that produces a list of the user's personal details (example: the city they live in, how old they are, their name, etc.), 
    or the user's personal preferences that are mentioned in their message. 
    Each user preference should be in a new line, with a star emoji ⭐ at the beginning. 
    If the user's message doesn't contain any information related to their preferences or personal details, then you MUST then respond with 'No new details.'.
    If the user has already mentioned the personal detail or preferences earlier in the chat, then you MUST respond with 'No new details.'.
    """

    # Keep history of the chat
    chat_history = [{"role": "system", "content": system_prompt}]

    for msg in messages:
        # Store the user's message
        chat_history.append({"role": "user", "content": msg})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )

        # Get the bot's response and store it
        bot_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_message})

        print("\nUser: ", msg)
        print("Bot:")
        print(bot_message)

user_messages = ["My name is Fred, and I enjoy long walks on the beach.", "Hello, how are you?", "I like strawberries", "I like strawberries"]

bot_v2(user_messages)
