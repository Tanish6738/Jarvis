from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
GorqAPIKey = env_vars.get("GorqAPIKey")

# Validate required API keys
if not GorqAPIKey:
    raise ValueError("GorqAPIKey not found in .env file")

# Initialize client
client = Groq(api_key=GorqAPIKey)

# Define system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open("Data/ChatLog.json", "r") as file:
        messages = load(file)
except:
    with open("Data/ChatLog.json", "w") as file:
        dump([], file)

def GoogleSearch(query):
    results = list(search(query, advanced=True , num_results=5))
    Answers = f"The search results for {query} are: \n[start]\n"
    for result in results:
        Answers += f"Title : {result.title}\n Description : {result.description}\n "
    return Answers

def AnswerModifier (Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified = "\n".join(non_empty_lines)
    return modified

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you today?"}
]

def Information ():
    data = ""
    current_date_time = datetime.datetime.now()
    Day = current_date_time.strftime("%A")
    Date = current_date_time.strftime("%d")
    Month = current_date_time.strftime("%B")
    Year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%I")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data += f"Use this Real-time Information if needed : \n"
    data += f"Day : {Day}\n"
    data += f"Date : {Date}\n"
    data += f"Month : {Month}\n"
    data += f"Year : {Year}\n"
    data += f"Time : {hour}:{minute}:{second}\n"
    return data

def RealtimeSearchEngine (query):
    global messages , SystemChatBot

    with open("Data/ChatLog.json", "r") as file:
        messages = load(file)
    messages.append({"role": "user", "content": f"{query}"})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "user", "content": Information()}] + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None    
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("\n", " ")
    messages.append({"role": "assistant", "content": Answer})

    with open("Data/ChatLog.json", "w") as file:
        dump(messages, file, indent=4)

    SystemChatBot.pop()

    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        print(RealtimeSearchEngine(query))