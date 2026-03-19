import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"



def chat_with_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(URL, headers=headers, json=data)

        if res.status_code != 200:
            return "api error: " + res.text

        response_json = res.json()

        if "choices" not in response_json:
            return "invalid response: " + str(response_json)

        return response_json["choices"][0]["message"]["content"]

    except Exception as e:
        return "error: " + str(e)


def detect_task(text):
    t = text.lower()

    if "summary" in t:
        return "summary"
    if "sentiment" in t:
        return "sentiment"
    if "explain code" in t or "bug" in t:
        return "code"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"

    return "chat"


def ask_followup():
    print("not clear what you want")
    print("1 -> summary")
    print("2 -> sentiment")
    print("3 -> explain code")
    choice = input("what should i do? ").strip()

    mapping = {"1": "summary", "2": "sentiment", "3": "code"}
    return mapping.get(choice, "chat")


def summarize(text):
    return chat_with_openrouter(
        f"give 1-line, 3 bullets, and 5 sentence summary:\n{text}"
    )


def sentiment(text):
    return chat_with_openrouter(
        f"give sentiment label, confidence and reason:\n{text}"
    )


def explain_code(code):
    return chat_with_openrouter(
        f"explain this code, bugs, and time complexity:\n{code}"
    )


def chat(q):
    return chat_with_openrouter(q)


def main():
    print("simple chat mode")

    while True:
        q = input("\nyou: ")

        if q in ["exit", "quit"]:
            break

        if not q.strip():
            continue

        task = detect_task(q)

        if task == "chat":
            ans = chat(q)
        elif task == "summary":
            ans = summarize(q)
        elif task == "sentiment":
            ans = sentiment(q)
        elif task == "code":
            ans = explain_code(q)
        elif task == "youtube":
            ans = "youtube transcript fetch not added yet"
        else:
            task = ask_followup()
            if task == "summary":
                ans = summarize(q)
            elif task == "sentiment":
                ans = sentiment(q)
            elif task == "code":
                ans = explain_code(q)
            else:
                ans = chat(q)

        print("\nbot:", ans)


if __name__ == "__main__":
    main()