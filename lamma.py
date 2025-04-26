# lamma.py
from groq import Groq
import os

client = Groq()

def generate_summary(input_text):
    """Generate summary using Groq/Llama"""
    if not input_text.strip():
        return "No transcript available to summarize."
        
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text:\n\n{input_text}. Also at the end give this was from which subject for example: Biology, Chemistry, etc."
                }
            ],
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"