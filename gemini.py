import google.generativeai as genai
import os

history_fresh = [{"role": "user", "parts": "Hello"},
{"role": "model", "parts": "Great to meet you. What would you like to know?"},
]

def ask_gemini(user_input):
    API_KEY = os.getenv("gemini_key")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text

def chat_gemini(user_input):

    API_KEY = os.getenv("gemini_key")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=history_fresh)

    response = chat.send_message(user_input)
    history_fresh.append({"role": "user", "parts": user_input})
    history_fresh.append({"role": "model", "parts": response.text})
    return response.text

def on_chat_close():
    history_fresh = [{"role": "user", "parts": "Hello"},
    {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
