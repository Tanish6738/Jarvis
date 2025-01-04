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