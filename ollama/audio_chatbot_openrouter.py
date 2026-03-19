import os
import requests
import speech_recognition as sr

apikey = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"



def chat_with_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)

        if res.status_code != 200:
            return "api error: " + res.text

        response_json = res.json()

        if "choices" not in response_json:
            return "invalid response: " + str(response_json)

        return response_json["choices"][0]["message"]["content"]

    except Exception as e:
        return "error: " + str(e)


def get_audio(fp):
    r = sr.Recognizer()

    try:
        with sr.AudioFile(fp) as src:
            audio = r.record(src)

        text = r.recognize_google(audio)

        if not text:
            return ""

        return text.strip()

    except Exception as e:
        print("error:", e)
        return ""


def summarize(text):
    return chat_with_openrouter(f"""
{text}
""")


def main():
    print("audio mode")

    while True:
        p = input("audio file path: ")

        if p == "quit":
            break

        if not p.strip():
            continue

        txt = get_audio(p)

        if not txt:
            print("failed to transcribe audio")
            continue

        print("\ntranscript:")
        print(txt)

        print("\nsummary:")
        print(summarize(txt))


if __name__ == "__main__":
    main()