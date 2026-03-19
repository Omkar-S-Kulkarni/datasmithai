import os
import requests
from pdf2image import convert_from_path
import pytesseract

# -------- CONFIG --------
POPPLER_PATH = r"C:\poppler\poppler\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"


# -------- OCR --------
def readPdf(p):
    imgs = convert_from_path(p, poppler_path=POPPLER_PATH)

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
    if total_chars > 0:
        confidence = min(100, total_chars / 50)

    return txt, round(confidence, 2)


# -------- OPENROUTER CALL --------
def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",   # safer model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(URL, headers=headers, json=data)

        # DEBUG (very important)
        if res.status_code != 200:
            print("API ERROR:", res.text)
            return "api error"

        response_json = res.json()

        if "choices" not in response_json:
            print("INVALID RESPONSE:", response_json)
            return "invalid response"

        return response_json["choices"][0]["message"]["content"]

    except Exception as e:
        return "error: " + str(e)

# -------- TASKS --------
def summarize(text):
    prompt = f"""Give output in this format:

1-line summary:
-

3 bullet points:
-
-
-

5 sentence summary:
{text}
"""
    return ask_llm(prompt)


def sentiment(text):
    prompt = f"sentiment label, confidence %, and one-line reason:\n{text}"
    return ask_llm(prompt)


# -------- MAIN --------
def main():
    print("pdf chatbot (openrouter)")

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

        print("text extracted")
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