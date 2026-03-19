import speech_recognition as sr
import ollama


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
    return ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[{
            "role": "user",
            "content": f"""Give output in this format:

1-line summary:
-

3 bullet points:
-
-
-

5 sentence summary:
{text}
"""
        }]
    )['message']['content']


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