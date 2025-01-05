import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os 
from time import sleep

def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg in Files:
        img_path = os.path.join(folder_path, jpg)
        try:
            # Using os.startfile instead of PIL.Image.show()
            abs_path = os.path.abspath(img_path)
            os.startfile(abs_path)
            sleep(1)
            print(f"Opening image: {img_path}")
        except Exception as e:
            print(f"Failed to open image {img_path}: {str(e)}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization" : f"Bearer {get_key('.env','HuggingFaceAPIKey')}"                               
}

async def query(payload):
    response = await asyncio.to_thread(requests.post , API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt : str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs" : f"{prompt} , quality = 4k ,sharpness =maximum ,Ultra High Details , high resolution , seed = {randint(0, 100000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i , image_bytes in enumerate(image_bytes_list):
        with open(f"Data/{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as file:
            file.write(image_bytes)

def GenerateImages(prompt):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

while True :
    try :
        with open("Frontend/Files/ImageGeneration.data", "r") as file:
            Data : str = file.read()
        
        Prompt , Status = Data.split(",")

        if Status == "True":
            print("Generating images")
            ImageStatus = GenerateImages(Prompt)

            with open("Frontend/Files/ImageGeneration.data", "w") as file:
                file.write("False,False")
                break
        else :
            sleep(1)

    except Exception as e:
        print(e)