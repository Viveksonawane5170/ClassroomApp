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

def generate_questions(input_text):
    """Generate questions based on the summary text"""
    if not input_text.strip():
        return "No summary available to generate questions from."
        
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"Based on the following summary, generate 5 meaningful questions that would test a student's understanding of the material:\n\n{input_text}\n\nFormat the questions clearly with numbers and ensure they cover key concepts from the summary."
                }
            ],
            temperature=0.5,  # Slightly higher temperature for more creative questions
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating questions: {str(e)}"