import os
import requests
from pdf2image import convert_from_path
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

poppler_path = r"C:\poppler\poppler\Library\bin"
api_key = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"


def readPdf(p):
    imgs = convert_from_path(p, poppler_path=poppler_path)

    txt = ""
    total_chars = 0

    for i, x in enumerate(imgs):
        try:
            t = pytesseract.image_to_string(x)
        except Exception:
            t = ""

        txt += "\nPAGE " + str(i + 1) + "\n" + t
        total_chars += len(t)

    confidence = 0
    confidence = total_chars / 50
    if confidence > 100:
        confidence = 100

    return txt, round(confidence, 2)



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
        res = requests.post(URL, headers=headers, json=data)

        if res.status_code != 200:
            return "api error: " + res.text

        response_json = res.json()

        try:
            return response_json["choices"][0]["message"]["content"]
        except:
            return ""

     

    except Exception as e:
        return "error: " + str(e)


def summarize(text):
    return call_api(f"""Give output in this format:

1-line summary:
                    
3 bullet points:


5 sentence summary:
{text}
""")


def sentiment(text):
    return call_api(
        f"sentiment label, confidence %, and one-line reason:\n{text}"
    )


def main():
    print("pdf chatbot")

    while True:
        p = input("pdf path: ")

        if p == "quit":
            break

        if not p.strip():
            continue

        text, conf = readPdf(p)

        if not text.strip():
            print("failed to extract text")
            continue

        print("done")
        print("OCR confidence:", conf, "%")

        while True:
            q = input("\nask: ")

            if q == "back":
                break

            if not q.strip():
                continue

            q_lower = q.lower()

            if "summary" in q_lower:
                print(summarize(text))
            elif "sentiment" in q_lower:
                print(sentiment(text))
            else:
                print("what do you want? summary or sentiment?")


if __name__ == "__main__":
    main()