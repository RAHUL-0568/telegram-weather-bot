from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TG_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
    r = requests.get(url).json()
    if r.get("cod") != 200:
        return "City not found."
    temp = r['main']['temp']
    desc = r['weather'][0]['description']
    return f"🌡️ {city.title()}: {temp}°C, {desc}"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text.startswith("/weather"):
            city = text.replace("/weather", "").strip()
            weather_info = get_weather(city)
            send_message(chat_id, weather_info)
    return "ok"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Weather bot is live!"

if __name__ == "__main__":
    app.run()
