import cohere  # Import the Cohere library for AI services.
from rich import print  # Import the Rich library to enhance terminal outputs.
from dotenv import dotenv_values  # Import dotenv to load environment variables.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("CohereApiKey")
co = cohere.Client(api_key="gWMhe9JkfCL0BNdmtYDdaPdhP5czy1MdtzaUn8xK")

# Define a list of recognized function keywords for task categorization.
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Initialize an empty list to store user messages.
messages = []

# Define the preamble that guides the AI model on how to categorize queries.

preamble = """
You are a very accurate Decision-Making Model created by My Master Tanishq Chouhan, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

# Define a chat history with predefined user-chatbot interaction for context.
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, open firefox."},
    {"role": "User", "message": "remind me that I have a dancing performance on 5th Aug at 11pm."},
    {"role": "Chatbot", "message": "reminder 11:00pm 5th Aug dancing performance."},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."},
    {"role": "User", "message": "who created you?"},
    {"role": "Chatbot", "message": "general who created you?"},
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "what can you do?"},
    {"role": "Chatbot", "message": "general what can you do?"},
    {"role": "User", "message": "are you an AI?"},
    {"role": "Chatbot", "message": "general are you an AI?"},
    {"role": "User", "message": "who is your creator?"},
    {"role": "Chatbot", "message": "general who is your creator?"},
    {"role": "User", "message": "who developed you?"},
    {"role": "Chatbot", "message": "general who developed you?"},
    {"role": "User", "message": "who made you?"},
    {"role": "Chatbot", "message": "general who made you?"},
    {"role": "User", "message": "how do you feel today?"},
    {"role": "Chatbot", "message": "general how do you feel today?"},
    {"role": "User", "message": "are you doing good?"},
    {"role": "Chatbot", "message": "general are you doing good?"}
]

def FirstLayerDWM(prompt: str = "test"):
    # Add the user's prompt to the message history.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        message=prompt,  # Add the required message parameter
        model="command",  # Changed from "command-plus" to "command"
        chat_history=ChatHistory,  # Provide the predefined chat history for context.
        prompt_truncation="off",  # Ensure the prompt is not truncated.
        connectors=[],  # No additional connectors are used.
        preamble=preamble  # Pass the detailed instruction preamble.
    )

    # Initialize an empty string to store the generated response.
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text  # Append generated text to the response.

    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", " ")
    response = response.split(",")

    # Strip leading and trailing whitespaces from each task.
    response = [i.strip() for i in response]

    # Initialize an empty list to filter valid tasks.
    temp = []
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)  # Add valid tasks to the filtered list.

    # Update the response with the filtered list of tasks.
    response = temp

    # If "query" is in the response, recursively call the function for further clarification.
    if "(query)" in response:
        new_response = FirstLayerDWM(prompt=prompt)
        return new_response  # Return the clarified response.

    # Return the response.
    return response

# Entry point for the script.
if __name__ == "__main__":
    while True:
        print(FirstLayerDWM(input(">>> ")))  # Print the categorized response.