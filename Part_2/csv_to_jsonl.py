import csv
import json


def csv_to_jsonl(file_input, file_output):
    SYSTEM_PROMPT = "Jada is a creator on Fanvue, chatting with one of her fans."

    JSON_OBJECTS = []

    with open(file_input) as file_in:
        # Open CSV file
        csv_reader = csv.DictReader(file_in)

        prev_sender = "fan"  # Initialise previous sender to be the fan

        fan_message = ""
        creator_message = ""
        chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for row in csv_reader:
            sender = row["sender_handle"]

            # State: Fan -> Fan
            if sender == "fan" and prev_sender == "fan":
                # Concatenate multiple messages from the fan
                fan_message += row["message"]

                prev_sender = "fan"
            # State: Creator -> Creator
            elif sender == "creator" and prev_sender == "creator":
                # Concatenate multiple messages from the creator
                creator_message += row["message"]

                prev_sender = "creator"
            # State: Fan -> Creator
            elif sender == "creator" and prev_sender == "fan":
                # Store fan message
                chat_messages.append({"role":"user", "content":fan_message})
                fan_message = ""  # Clear fan message

                # Concatenate current creator message
                creator_message += row["message"]

                prev_sender = "creator"
            # State: Creator -> Fan
            elif sender == "fan" and prev_sender == "creator":
                # Store creator message
                chat_messages.append({"role":"assistant", "content":creator_message})
                creator_message = ""  # Clear creator message

                # Concatenate current fan message
                fan_message += row["message"]

                # Store chat messages of fan and creator
                JSON_OBJECTS.append({"messages": chat_messages})

                # Reset chat messages
                chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

                prev_sender = "fan"

    # Write chat messages to JSONL file
    with open(file_output, 'w') as file_out:
        for chat_message in JSON_OBJECTS:
            json.dump(chat_message, file_out)
            file_out.write('\n')  # Add new line for JSONL format
    
    print("Converted from CSV to JSONL file.")


FILE_INPUT = "../fan_creator_chat.csv"
FILE_OUTPUT = "../fan_creator_chat.jsonl"

csv_to_jsonl(FILE_INPUT, FILE_OUTPUT)