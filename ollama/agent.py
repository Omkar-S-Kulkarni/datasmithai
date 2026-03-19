import os
import time
import requests

MAX_CHARS = 2000

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"


def ollama_call(messages, retries=2):
    for attempt in range(retries):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 300   # similar to num_predict
            }

            res = requests.post(URL, headers=headers, json=data)

            if res.status_code != 200:
                raise Exception(res.text)

            response_json = res.json()

            if "choices" not in response_json:
                raise Exception(str(response_json))

            return response_json["choices"][0]["message"]["content"]

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return f"Error: {str(e)}"


def detect_intent(text):
    t = text.lower()
    if "summary" in t:
        return "summary"
    if "sentiment" in t:
        return "sentiment"
    if "explain" in t or "bug" in t or "code" in t:
        return "code"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"
    return "unknown"


def needs_clarification(intent, text):
    if intent == "unknown":
        return True
    if len(text.split()) < 5:
        return True
    return False


def ask_followup():
    return "What do you want me to do? (summary / sentiment / explain code)"


def summarize(text):
    return ollama_call([{
        "role": "user",
        "content": f"Give a 1-line summary, 3 bullet points, and a 5 sentence summary:\n{text[:MAX_CHARS]}"
    }])


def sentiment(text):
    return ollama_call([{
        "role": "user",
        "content": f"Give sentiment label, confidence %, and one-line reason:\n{text[:MAX_CHARS]}"
    }])


def explain_code(code):
    return ollama_call([{
        "role": "user",
        "content": f"Explain this code, find bugs, and give time complexity:\n{code[:MAX_CHARS]}"
    }])


def chat(text):
    return ollama_call([{
        "role": "user",
        "content": text[:MAX_CHARS]
    }])


def run_agent(text):
    logs = []

    logs.append("Step 1: Detecting intent")
    intent = detect_intent(text)
    logs.append(f"Intent: {intent}")

    if needs_clarification(intent, text):
        return {"followup": ask_followup(), "logs": logs}

    logs.append("Step 2: Executing task")

    if intent == "summary":
        result = summarize(text)
    elif intent == "sentiment":
        result = sentiment(text)
    elif intent == "code":
        result = explain_code(text)
    elif intent == "youtube":
        result = "YouTube transcript not implemented yet"
    else:
        result = chat(text)

    logs.append("Step 3: Done")

    return {"result": result, "logs": logs}