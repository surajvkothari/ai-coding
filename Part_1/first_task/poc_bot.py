from openai import OpenAI


def bot(msg):
    client = OpenAI()

    system_prompt = """You are an assistant that produces a list of the user's personal details (example: the city they live in, how old they are, their name, etc.), 
    or the user's personal preferences that are mentioned in their message. 
    Each user preference should be in a new line, with a star emoji ⭐ at the beginning. 
    If the user's message doesn't contain any information related to their preferences or personal details, then you MUST then respond with 'No new details.'
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": msg}
        ]
    )

    return response.choices[0].message.content


user_messages = ["My name is Fred, and I enjoy long walks on the beach.", "Hello, how are you?", "I like strawberries", "I like strawberries"]

for m in user_messages:
    print("\nUser:", m)
    print("Bot:")
    print(bot(m))
