from groq import Groq
from json import load , dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GorqAPIKey = env_vars.get("GorqAPIKey")

client = Groq(api_key=GorqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {
        "role": "system", "content": System
    }
]

try:
    with open("Data/ChatLog.json", "r") as file:  # Use forward slashes
        messages = load(file)  # Correct JSON loading
except:
    with open("Data/ChatLog.json", "w") as file:
        dump([], file)  # Write the dumped JSON string

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%I")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed\n"
    data += f"Day: {day}\n Date: {date}\n Month: {month}\n Year: {year}\n Time: {hour}:{minute}:{second}\n"
    
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """
    This function sends the user's query to the chatbot model and returns the response.
    """
    try:
        with open("Data/ChatLog.json", "r") as file:  # Use forward slashes
            messages = load(file)  # Correct JSON loading

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [
                {
                    "role": "system",  # Changed from "System" to "system"
                    "content": RealtimeInformation()
                }
            ] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion :
            if chunk.choices[0].delta.content :
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", " ")

        messages.append({"role": "assistant", "content": Answer})


        with open("Data/ChatLog.json", "w") as file:  # Use forward slashes
            dump(messages, file, indent=4)  # Write the dumped JSON string

        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        if not messages:  # Only initialize if empty
            with open("Data/ChatLog.json", "w") as file:  # Use forward slashes
                dump([], file)  # Write the dumped JSON string
            messages = []
        return ChatBot(Query)
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter your query / question: ")
        print(ChatBot(user_input))