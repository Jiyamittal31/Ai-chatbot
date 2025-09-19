from src.chatbot_core import Chatbot

def test_response_type():
    bot = Chatbot()
    resp, score = bot.get_response("hello")
    assert isinstance(resp, str)
    assert isinstance(score, float)
 
