import tkinter as tk
from chatbot_core import Chatbot

bot = Chatbot("SmartBot")

def send_message():
    user_input = entry.get()
    if not user_input:
        return
    chat_box.insert(tk.END, f"You: {user_input}\n")
    response = bot.get_response(user_input)
    chat_box.insert(tk.END, f"{bot.name}: {response}\n\n")
    entry.delete(0, tk.END)

# UI Setup
root = tk.Tk()
root.title("Smart Chatbot")
root.geometry("500x600")

chat_box = tk.Text(root, bg="black", fg="lime", font=("Consolas", 12))
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame = tk.Frame(root)
frame.pack(pady=5)

entry = tk.Entry(frame, width=40, font=("Arial", 14))
entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

root.mainloop()
