from groq import Groq

client = Groq()

# The text you want to summarize
input_text = """"""

completion = client.chat.completions.create(
    model="llama3-70b-8192",  # Updated model name
    messages=[
        {
            "role": "user",
            "content": f"Please provide a concise summary of the following text:\n\n{input_text}. Also at the end give this was from which subject for example: Biology, Chemistry, etc."
        }
    ],
    temperature=0.3,  # Lower temperature for more focused summaries
    max_tokens=1024,
    top_p=1,
    stream=False,  # No need to stream for summaries
    stop=None,
)

print(completion.choices[0].message.content)