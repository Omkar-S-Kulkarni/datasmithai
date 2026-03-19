import ollama
from pdf2image import convert_from_path
import pytesseract

POPPLER_PATH = r"C:\poppler\poppler\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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


def sentiment(text):
    return ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[{
            "role": "user",
            "content": f"sentiment label, confidence %, and one-line reason:\n{text}"
        }]
    )['message']['content']


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