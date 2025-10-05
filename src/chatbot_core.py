import requests
import wikipedia

# API KEYS
OPENWEATHER_KEY="cebccec146b3e4df5b7fe8d87a7c9fce"
NEWSAPI_KEY="70bd4ba3cb02471386222def02c2cab6"

class Chatbot:
    def __init__(self, name="SmartBot"):
        self.name = name

    def get_response(self, query: str) -> str:
        query = query.lower().strip()

        # Handle slash commands
        if query.startswith("/weather"):
            city = query.replace("/weather", "").strip() or "Delhi"
            return self._get_weather(city)

        elif query.startswith("/news"):
            topic = query.replace("/news", "").strip() or "technology"
            return self._get_news(topic)

        elif query.startswith("/wiki"):
            topic = query.replace("/wiki", "").strip()
            return self._get_wiki(topic)

        # Small talk
        elif query in ["hi", "hello", "hey"]:
            return "Hello! How can I help you today?"

        elif query in ["bye", "exit"]:
            return "Goodbye! Have a great day!"

        # Default fallback: try Wikipedia summary
        else:
            return self._get_wiki(query)

    # APIs
    def _get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
            res = requests.get(url).json()
            if res.get("cod") != 200:
                return f"Weather not found for {city}"
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"Weather in {city}: {temp}°C, {desc}"
        except Exception as e:
            return f"Error fetching weather: {e}"

    def _get_news(self, topic):
        try:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
            res = requests.get(url).json()
            if res.get("status") != "ok":
                return f"News not found for {topic}"
            articles = res["articles"][:3]
            headlines = [f"- {a['title']}" for a in articles]
            return f"Top news about {topic}:\n" + "\n".join(headlines)
        except Exception as e:
            return f"Error fetching news: {e}"

    def _get_wiki(self, topic):
        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return "I couldn't find info on that."
