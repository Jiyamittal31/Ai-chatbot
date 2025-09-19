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



while True:
    query = input("You: ").strip().lower()

    if query == "exit":
        print("Bot: Bye!")
        break
    elif query.startswith("/weather"):
        city = query.replace("/weather", "").strip() or "Delhi"
        print("Bot:", _get_weather(city))
    elif query.startswith("/news"):
        topic = query.replace("/news", "").strip() or "technology"
        print("Bot:", _get_news(topic))
    else:
        # fallback to normal response
        print("Bot:", get_response(query))

