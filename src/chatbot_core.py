import os, json, string, joblib, numpy as np, nltk, random, webbrowser, ast
from datetime import datetime
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

for pkg, res in [("punkt", "tokenizers/punkt"),
                 ("wordnet", "corpora/wordnet"),
                 ("omw-1.4", "corpora/omw-1.4"),
                 ("stopwords", "corpora/stopwords")]:
    try: nltk.data.find(res)
    except LookupError: nltk.download(pkg)

class Chatbot:
    def __init__(self, corpus_path="data/corpus.txt", intent_path="data/intents.json",
                 cache_dir="cache", threshold=0.2, bot_name="Buddy Chatbot"):
        self.bot_name = bot_name
        self.theme = {"primary_color": "#0b5cff", "background": "#ffffff"}
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.punct_table = str.maketrans("", "", string.punctuation)
        self.corpus = self._load_lines(corpus_path)
        self.intents = self._load_json(intent_path)
        self.vectorizer, self.tfidf = self._build_vectorizer(cache_dir)
        self.threshold = threshold
        self.jokes = [
           	"I’d tell you a UDP joke, but you might not get it.",
            	"Why did the developer go broke? Because he used up all his cache.",
            	"Why do programmers prefer dark mode? Because light attracts bugs.",
	    	"Why was the mobile phone wearing glasses?... Because it lost its contacts.",
		"What was the spider doing on the computer?... He was making a web-site!",
		"What do you call an iPhone that sleeps too much?... Dead Siri-ous.",
		"What did the computer have during his break time?... He had a byte!",
		"What is the computer's favorite snack to eat?... Microchips!",
		"What shoes do computers love the most?... Re-boots!",
		"Why did the computer go to the dentist?... To get his Bluetooth checked."
		        ]

    def _load_lines(self, path):
        if os.path.exists(path):
            return [line.strip() for line in open(path, encoding="utf-8") if line.strip()]
        return ["Hello! How can I help you today?"]

    def _load_json(self, path):
        if os.path.exists(path):
            return json.load(open(path, encoding="utf-8"))
        return {}

    def _preprocess(self, text):
        text = text.lower().translate(self.punct_table)
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens if t.isalnum() and t not in self.stop_words]
        return tokens

    def _build_vectorizer(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        vec_path, tfidf_path, snapshot = os.path.join(cache_dir, "vec.joblib"), os.path.join(cache_dir, "tfidf.joblib"), os.path.join(cache_dir, "corpus.snap")
        try:
            saved = joblib.load(snapshot)
        except Exception:
            saved = None
        if os.path.exists(vec_path) and os.path.exists(tfidf_path) and saved == self.corpus:
            return joblib.load(vec_path), joblib.load(tfidf_path)
        v = TfidfVectorizer(tokenizer=self._preprocess, lowercase=False)
        t = v.fit_transform(self.corpus)
        joblib.dump(v, vec_path); joblib.dump(t, tfidf_path); joblib.dump(self.corpus, snapshot)
        return v, t

    # safe evaluate arithmetic expressions
    def _safe_eval(self, expr):
        try:
            node = ast.parse(expr, mode="eval")
        except Exception:
            return "Invalid expression."

        def _eval(n):
            if isinstance(n, ast.Expression):
                return _eval(n.body)
            if isinstance(n, ast.Constant):  # python3.8+
                if isinstance(n.value, (int, float)):
                    return n.value
                raise ValueError("Invalid constant")
            if isinstance(n, ast.Num):  # older python
                return n.n
            if isinstance(n, ast.BinOp):
                left, right = _eval(n.left), _eval(n.right)
                if isinstance(n.op, ast.Add): return left + right
                if isinstance(n.op, ast.Sub): return left - right
                if isinstance(n.op, ast.Mult): return left * right
                if isinstance(n.op, ast.Div): return left / right
                if isinstance(n.op, ast.Mod): return left % right
                if isinstance(n.op, ast.Pow): return left ** right
                if isinstance(n.op, ast.FloorDiv): return left // right
                raise ValueError("Unsupported operator")
            if isinstance(n, ast.UnaryOp):
                val = _eval(n.operand)
                if isinstance(n.op, ast.UAdd): return +val
                if isinstance(n.op, ast.USub): return -val
                raise ValueError("Unsupported unary op")
            raise ValueError("Unsupported expression")
        try:
            return str(_eval(node))
        except Exception:
            return "Error evaluating expression."

    def _handle_slash_command(self, text):
        parts = text.strip().split(maxsplit=1)
        cmd = parts[0][1:].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""
        if cmd in ("name", "botname"):
            return f"My name is {self.bot_name}."
        if cmd in ("setname", "rename"):
            if not arg: return "Usage: /setname YourBotName"
            self.bot_name = arg
            return f"Okay — I will use the name: {self.bot_name}"
        if cmd == "time":
            return datetime.now().strftime("%H:%M:%S")
        if cmd == "date":
            return datetime.now().strftime("%Y-%m-%d")
        if cmd == "joke":
            return random.choice(self.jokes)
        if cmd == "calc":
            if not arg: return "Usage: /calc 2+2*3"
            return self._safe_eval(arg)
        if cmd == "open":
            if not arg: return "Usage: /open https://example.com"
            try:
                webbrowser.open(arg)
                return f"Opening {arg}"
            except Exception:
                return "Unable to open the URL on this system."
        if cmd == "help":
            return ("/help, /name, /setname <name>, /time, /date, /joke, "
                    "/calc <expr>, /open <url>, also ask normal questions.")
        if cmd == "theme":
            if not arg: return "Usage: /theme #RRGGBB (or use Streamlit sidebar)"
            self.theme["primary_color"] = arg
            return f"Theme primary color set to {arg}"
        return "Unknown command. Type /help for commands."

    def _match_intent(self, user_input):
        ui = user_input.lower()
        for intent, data in self.intents.items():
            for pat in data.get("patterns", []):
                if pat in ui:
                    responses = data.get("responses", [])
                    if responses:
                        return random.choice(responses)
        return None

    def get_response(self, user_input):
        ui = (user_input or "").strip()
        if not ui:
            return "Please say something.", 0.0
        if ui.startswith("/"):
            return self._handle_slash_command(ui), 1.0
        intent_resp = self._match_intent(ui)
        if intent_resp:
            return intent_resp, 1.0
        user_vec = self.vectorizer.transform([ui])
        sims = cosine_similarity(user_vec, self.tfidf).flatten()
        best_idx = int(np.argmax(sims))
        best_score = float(np.max(sims))
        if best_score < self.threshold:
            return "Sorry, I don't understand. Try /help.", best_score
        return self.corpus[best_idx], best_score

    def set_theme(self, primary_color=None, background=None):
        if primary_color: self.theme["primary_color"] = primary_color
        if background: self.theme["background"] = background

    def set_name(self, name):
        self.bot_name = name
