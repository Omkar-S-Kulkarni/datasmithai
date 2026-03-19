import os
import requests
api_key = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"



def call_api(prompt):
    headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url,headers=headers,json=data)

        if res.status_code != 200:
            print("error:", res.text)
            return ""

        response_json = res.json()

        try:
            return response_json["choices"][0]["message"]["content"]
        except:
            return ""









        

    except Exception as e:
        return "error: " + str(e)


def detect_task(text):
    t = text.lower()

    if "summary" in t:
        return "summary"
    elif "sentiment" in t:
        return "sentiment"
    elif "code" in t or "bug" in t:
        return "code"
    elif "youtu" in t:
        return "youtube"

    return "chat"


def ask_followup():
    print("not clear what you want")
    print("1 -> summary")
    print("2 -> sentiment")
    print("3 -> explain code")
    choice = input("what should i do? ").strip()

    if choice == "1":
        return "summary"
    elif choice == "2":
        return "sentiment"
    elif choice == "3":
        return "code"
    return "chat"


def summarize(text):
    return call_api("summarize this:\n" + text)


def sentiment(text):
    return call_api(
        f"give sentiment label, confidence and reason:\n{text}"
    )


def explain_code(code):
    return call_api(
        f"explain this code, bugs, and time complexity:\n{code}"
    )


def chat(q):
    return call_api(q)


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
            ans = "not added yet"
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



    