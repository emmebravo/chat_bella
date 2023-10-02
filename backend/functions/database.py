import json
import random


# get recent msg
def get_recent_messages():
    file_name = "stored_data.json"

    # learn instructions
    instructions = {
        "role": "system",
        "content": "You are interviewing the user for a job as an administrative assistant. Ask short questions that are related to the entry-level position. Your name is Bella, the user is called Eve. Keep your answers under 30.",
    }

    # initialize
    messages = []

    # randomize content
    ran = random.uniform(0, 1)
    if ran < 0.50:
        instructions["content"] = (
            instructions["content"] + " your response will include some dry humor."
        )
    else:
        instructions["content"] = (
            instructions["content"]
            + " your response will include a challenging question."
        )

    # append instructions to messages
    messages.append(instructions)

    # get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # append last 3 items of data
            if data:
                if len(data) < 3:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-3:]:
                        messages.append(item)
    except Exception as error:
        print(error)
        pass

    return messages


# store messages
def store_messages(req_message, res_message):
    file_name = "store_data.json"
    messages = get_recent_messages()[1:]

    # add to data
    user_message = {"role": "user", "content": req_message}
    assistant_message = {"role": "assistant", "content": res_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # save update file
    with open(file_name, "w") as file:
        json.done(messages, file)


# reset
def reset_messages():
    open("stored_data.json", "w")
