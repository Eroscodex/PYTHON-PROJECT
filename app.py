from flask import Flask, render_template, request, jsonify # type: ignore
import ollama # type: ignore

app = Flask(__name__)

messages = [
    {
        'role': 'system',
        'content': """You are Tech_Assistant — an assistant that MUST ONLY answer questions related to
laptop and PC e-commerce websites.

STRICT RULES:

1. Only answer allowed topics (laptops, PCs, PC parts, specifications, pricing, inventory, e-commerce issues, SEO, UX, product compatibility).
2. If the message is NOT about allowed topics, reply EXACTLY:
   "Sorry — this question is not related to our topics."
3. Always provide short, clear, ChatGPT-style responses.
4. Format lists and specs using Markdown-style bullets (e.g., *, -, 1.) for easy display in web chat.
"""
    }
]

ALLOWED_KEYWORDS = [
    "laptop", "pc", "computer", "ssd", "ram", "gpu", "cpu",
    "motherboard", "psu", "graphics card", "desktop", "notebook",
    "gaming pc", "ecommerce", "checkout", "shipping", "return",
    "warranty", "seo", "inventory", "stock", "product page",
    "acer", "dell", "hp", "lenovo", "asus", "macbook", "apple",
    "msi", "razer", "gigabyte", "samsung", "toshiba", "sony",
    "lg", "huawei", "xiaomi", "alienware"
]

greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']

def is_allowed(message):
    msg = message.lower()
    return any(keyword in msg for keyword in ALLOWED_KEYWORDS)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": ""})

    if user_input.lower() in greetings:
        assistant_response = "Hey! What's up?"
        messages.append({'role': 'user', 'content': user_input})
        messages.append({'role': 'assistant', 'content': assistant_response})
        return jsonify({"reply": assistant_response})

    if not is_allowed(user_input):
        return jsonify({"reply": "Sorry — this question is not related to our topic. BOBO KA?"})

    messages.append({'role': 'user', 'content': user_input})

    response = ollama.chat(
        model='Tech_Assistant:latest',
        messages=messages
    )

    assistant_response = getattr(response, 'content', None) or response.get('message', {}).get('content', '')

    messages.append({'role': 'assistant', 'content': assistant_response})

    return jsonify({"reply": assistant_response})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
