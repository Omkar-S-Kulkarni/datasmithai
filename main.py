from audio_chatbot_openrouter import main as audio_mode
from image_openrouter import main as image_mode
from main_chatbot_openrouter import main as chat_mode


def run():
    while True:
        print("\n1 audio")
        print("2 pdf")
        print("3 chat")
        print("0 exit")

        ch = input("choose: ").strip()

        if ch == "1":
            audio_mode()
        elif ch == "2":
            image_mode()
        elif ch == "3":
            chat_mode()
        elif ch == "0":
            break
        else:
            print("invalid choice, try again")


if __name__ == "__main__":
    run()