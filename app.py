import feedparser
from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "525c6e51ba0fc34e2e4919b85d11b73c"
CITY = "Delhi"

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=5).json()

        if "weather" not in data:
            print("Weather API error:", data)
            return "Unavailable", "--"

        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        return weather, temp

    except Exception as e:
        print("Weather exception:", e)
        return "Error", "--"

def get_headlines():
    try:
        feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(feed_url)

        headlines = []
        for entry in feed.entries[:5]:
            headlines.append(entry.title)

        return headlines

    except Exception as e:
        print("News exception:", e)
        return []

@app.route("/")
def home():
    time_now = datetime.now().strftime("%H:%M:%S")
    date_today = datetime.now().strftime("%d %B %Y")

    weather, temp = get_weather()
    headlines= get_headlines()

    if weather == "Rain":
        avatar = "rain.png"
    elif weather == "Clouds":
        avatar = "cloudy.png"
    elif weather == "Clear":
        avatar = "sunny.png"
    else:
        avatar = "default.png"

    return render_template(
        "index.html",
        time=time_now,
        date=date_today,
        weather=weather,
        temp=temp,
        avatar=avatar,
	headlines=headlines
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
