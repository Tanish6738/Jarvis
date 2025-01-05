from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicropohoneStatus,
    AnswerModifier,
    QueryModifier,
    GetAssistantStatus,
    GetMicrophoneStatus
)
from Backend.Model import FirstLayerDWM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.TextToSpeech import TextToSpeech
from Backend.Chatbot import ChatBot
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import os
import json
import threading

env_vars = dotenv_values(".env")
Username    = env_vars.get("Username")
AssistantName = env_vars.get("AssistantName")
DefaultMessage = f'''{Username} : Hello {AssistantName}! , How are you?
{AssistantName} : Welcome {Username}. I am doing well. How may i help you? '''
process_list = []  # New name for storing processes
Functios = ["open", "close", "content", "play", "system", "google search" , "youtube search" ]

def ShowDefaultIfNoChats():
    File = open(f"Data/ChatLog.json", "r", encoding="utf-8")
    if len(File.read()) < 5 :
        with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as File:
            File.write('')

        with open(TempDirectoryPath("Database.data"), "a", encoding="utf-8") as File:
            File.write(DefaultMessage)

def ReadChatLogJson():
    with open("Data/ChatLog.json", "r", encoding="utf-8") as File:
        chat_log_data = json.load(File)

    return chat_log_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chat_log = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chat_log += f"{Username} : {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chat_log += f"{AssistantName} : {entry['content']}\n"
    
    formatted_chat_log= formatted_chat_log.replace("User", Username + " ")
    formatted_chat_log= formatted_chat_log.replace("Assistant", AssistantName + " ")

    with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as File:
        File.write(AnswerModifier(formatted_chat_log))

def ShowChatOnGui():
    File = open(TempDirectoryPath("Database.data"), "r", encoding="utf-8")
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result='\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath("Database.data"), "w", encoding="utf-8")
        File.write(result)
        File.close()

def InitialExecution():
    SetMicropohoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultIfNoChats()
    ChatLogIntegration()
    ShowChatOnGui()

InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening ... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ... ")
    Decision = FirstLayerDWM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    Mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functios):
                run(Automation(list(Decision)))
    
    if ImageExecution:
        with open("Frontend/Files/ImageGeneration.data", "w") as File:
            File.write(f"{ImageGenerationQuery},True")

        try:
            process = subprocess.Popen(
                ["python", "Backend/ImageGeneration.py"],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False
            )
            # Use process_list instead of subprocess
            process_list.append(process)
        except Exception as e:
            print(f"Error Starting ImageGeneration.py : {e}")
    
    if G and R or R :

        SetAssistantStatus("Searching ... ")
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{AssistantName} : {Answer}")
        SetAssistantStatus("Answering ... ")
        TextToSpeech(Answer)
        return True
    else :
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking ... ")
                QueryFinal = Queries.replace("general", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering ... ")
                TextToSpeech(Answer)
                return True

            elif "realtime" in Queries:
                SetAssistantStatus("Searching ... ")
                QueryFinal = Queries.replace("realtime", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering ... ")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Goodbye Sir!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{AssistantName} : {Answer}")
                SetAssistantStatus("Answering ... ")    
                TextToSpeech(Answer)
                SetAssistantStatus("Answering ... ")
                os._exit(1)

    
def FirstThread():
    while True:

        currentStatus = GetMicrophoneStatus()

        if currentStatus == "True":
            MainExecution()
        else :
            AiStatus = GetAssistantStatus()

            if "Available" in AiStatus:
                sleep(0.1)
            else : 
                SetAssistantStatus("Available")

def SecondThread():

    GraphicalUserInterface()

if __name__ == "__main__":
    therad2 = threading.Thread(target=FirstThread , daemon=True)
    therad2.start()
    SecondThread()