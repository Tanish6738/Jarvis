from AppOpener import close , open as appopen
from webbrowser import open as webopen
from pywhatkit import search , playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import requests
import os
import keyboard
import asyncio
import subprocess

env_vars = dotenv_values(".env")
GorqAPIKey = env_vars["GorqAPIKey"]

classes = [
    "zCubwf", "hgKElc","LTKOO sY7ric" , "tw-text-small", "Z0LcW" , "gsrt vk_bk FzvWSB YwPhnf" , "pclqee",
    "tw-Data-text tw-text-small tw-ta"
    "IZ6rdc", "O5uR6d LTKOO" , "vlzY6d", "webanswers-webanswers_table__webanswers-table__webanswers-table",
    "dDono ikb4Bb gsrt" , "sXLaOe"
    "LWkfKe",  "VQF4g", "qv3Wpe", "kno-rdsc", "SPZz6b"
]

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

client = Groq(api_key=GorqAPIKey)

professional_response = [
    "Your satifaction is My priority; feel free to reach out to me anytime for any query",
    "I am at your service; feel free to reach out to me anytime for any query",
    "i am at your service for any additional questions or support you may need don't hesitate to reach out to me",
]

messages = []

SystemChatBot = [{
    "role": "system",  # Fixed typo 'systen'
    "content": f"Hello, I am {env_vars['Username']}, You're a content writer, you have to write content like "  # Fixed typo 'conten' and using env_vars instead of os.environ
}]

def GoogleSearch(query):
    search(query)
    return True

def Content(Topic):
    
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({
            "role" : "user","content" : f"{prompt}"
        })

        completion = client.chat.completions.create(
                            model="llama3-70b-8192",  
                            messages=SystemChatBot + messages,  # Using + operator correctly
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

        Answer = Answer.replace("</s>" , "")
        messages.append({
            "role" : "assistant", "content" : f"{Answer}"
        })
        return Answer
    Topic: str = Topic.replace("Content" , "")
    ContentByAi = ContentWriterAI(Topic)

    with open(f"Data/{Topic.lower().replace(' ', '')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAi)
        file.close()
    
    OpenNotepad(f"Data/{Topic.lower().replace(' ', '')}.txt")
    return True


def OpenApp(Topic):
    Url4Search = f"http://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def SearchYoutube(Topic):
    query = Topic.strip()
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return True

def PlayYoutube(Topic):
    query = Topic.strip()  # Clean the input
    try:
        playonyt(query)
    except Exception as e:
        print(f"Error playing YouTube video: {e}")
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
    return True

# PlayYoutube("binks sake")

def OpenApp(app, sess=requests.session()):
    try:
        # Attempt to open the app directly
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error opening app directly: {e}")

        # Helper function to extract links
        def extract_links(html):
            if html is None:
                return []
            
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a", {'jsname': 'UWckNb'})
            hrefs = [link.get("href") for link in links if link.get("href")]
            return hrefs
            
        # Helper function to perform Google search
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            try:
                response = sess.get(url, headers=headers)
                return response.text if response.status_code == 200 else None
            except Exception as e:
                print(f"Error during Google search: {e}")
                return None
        
        # Perform search and extract links
        html = search_google(app)
        links = extract_links(html)
        
        if links:
            # Open the first link
            full_url = f"https://www.google.com{links[0]}" if links[0].startswith('/url') else links[0]
            print(f"Opening: {full_url}")
            webbrowser.open(full_url)
        else:
            # Fallback to search result page
            fallback_url = f"https://www.google.com/search?q={app}"
            print(f"No specific links found. Opening search results: {fallback_url}")
            webbrowser.open(fallback_url)
        
        return True

def CloseApp(app):
    
    if "chrome" in app:
        pass
    else : 
        try : 
            close(app, match_closest=True, output=True, throw_error=True)
        except :
            return True

def System (command):

    def mute():
        keyboard.press_and_release("volume mute")
    
    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands : list[str]) :

    funcs = []

    for command in commands:
        if command.startswith("open") :
            if "open it" in command:
                pass
            if "open file" == command :
                pass
            else :
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general ") :
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close ") :
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play ") :
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content ") :
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search") :
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
        
        elif command.startswith("youtube search") :
            fun = asyncio.to_thread(SearchYoutube, command.removeprefix("youtube search"))
            funcs.append(fun)

        elif command.startswith("system ") :
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        
        else :
            print(f"No function found for command {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else : 
            yield result

async def Automation (commands : list[str]) :
    
    async for result in TranslateAndExecute(commands):
        pass 

    return True

# OpenApp("FaceBook")