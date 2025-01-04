import cohere

co = cohere.ClientV2("")
response = co.chat(
    model="command-r-plus", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response)
