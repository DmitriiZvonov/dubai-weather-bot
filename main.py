import vk_api
import requests
import schedule
import time
from datetime import datetime, timedelta

# ================= НАСТРОЙКИ =================
VK_TOKEN = "vk1.a.GpXji44Pfs8CvNddLvUvBTFegnCSf9q5_uzhryyLzEV_3dJ9WoJmC58mfp0oN1x7y7yWluIJvrhK0iFIGnMw44P1ac16ofEup3solM3mCVG0Td5GiRxB3NbTzLyvjLqAbvHqlDQqkXXn6ODvm58n9cW3XLNYhQ92lv2ENzlMIr_TOgJzeroL53IbxRQ_47MqYb8ctTIcKx36zN36BuMUmA"
GROUP_ID = "228816972"
WEATHER_API_KEY = "3cbf1f5ccd9356a53c4a3ff85b9c1b21"
CITY = "Dubai"
TIME_TO_POST = "04:00" 
# =============================================

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        res = requests.get(url).json()
        
        temp = round(res["main"]["temp"])
        feels_like = round(res["main"]["feels_like"])
        desc = res["weather"][0]["description"].capitalize()
        humidity = res["main"]["humidity"]
        wind = res["wind"]["speed"]
        
        sunrise = (datetime.fromtimestamp(res["sys"]["sunrise"]) + timedelta(hours=4)).strftime('%H:%M')
        sunset = (datetime.fromtimestamp(res["sys"]["sunset"]) + timedelta(hours=4)).strftime('%H:%M')

        if temp > 35:
            advice = "☀️ Сегодня будет жарко! Не забывайте SPF и пейте больше воды."
        elif wind > 7:
            advice = "💨 Ожидается свежий ветер. Идеальное время для прогулки у моря."
        else:
            advice = "✨ Погода шепчет: отличное время для завтрака на террасе или прогулки по городу!"

        text = (
            f"☀️ ДОБРОЕ УТРО, ДУБАЙ! ☀️\n\n"
            f"📅 Сегодня: {datetime.now().strftime('%d.%m.%Y')}\n"
            f"📍 Локация: Дубай, ОАЭ\n\n"
            f"🌡 Температура воздуха: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"☁️ На небе: {desc}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с\n\n"
            f"🌅 Восход: {sunrise} | Закат: {sunset}\n\n"
            f"{advice}\n\n"
            f"Пусть этот день принесет вам только яркие эмоции! Будьте в курсе событий вместе с нами. 🇦🇪\n\n"
            f"#Дубай #Погода #ДубайНаЛадони #ОАЭ #Dubai #UAE #DubaiWeather"
        )
        return text
    except Exception as e:
        print(f"Ошибка получения погоды: {e}")
        return None

def post_to_vk():
    message = get_weather()
    if not message:
        print("Не удалось подготовить сообщение.")
        return

    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()
        vk.wall.post(owner_id=-int(GROUP_ID), from_group=1, message=message)
        print(f"✅ Пост успешно опубликован в {datetime.now()}")
    except Exception as e:
        print(f"❌ Ошибка публикации в ВК: {e}")

schedule.every().day.at(TIME_TO_POST).do(post_to_vk)

print(f"🤖 Бот запущен! Он будет публиковать пост ежедневно в {TIME_TO_POST} (по UTC).")

while True:
    schedule.run_pending()

    time.sleep(30)
    import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Создаем простейший веб-сервер, чтобы Render не выключал бота
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Запускаем сервер в отдельном потоке, чтобы он не мешал боту
threading.Thread(target=run_server, daemon=True).start()
