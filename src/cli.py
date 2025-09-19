from chatbot_core import Chatbot

def main():
    bot = Chatbot()
    print(f"{bot.bot_name} ready. Type /help to see commands. Type 'exit' to quit.")
    while True:
        user = input("You: ").strip()
        if not user: continue
        if user.lower() in ("exit", "quit"):
            print(f"{bot.bot_name}: Bye!")
            break
        resp, _score = bot.get_response(user)
        print(f"{bot.bot_name}: {resp}")

if __name__ == "__main__":
    main()
