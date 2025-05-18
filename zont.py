import requests

def get_weather(lat, lon):
    api_key = "21666ca75a71c32f0028e44774beae49"  # Замените на ваш API-ключ
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ru"
    
    try:
        response = requests.get(url)
        weather_data = response.json()

        # Проверка на дождь в данных прогноза
        if "rain" in weather_data:
            rain_volume = weather_data["rain"].get("1h", 0)  # Объем дождя за 1 час
            if rain_volume > 0:
                return "Возьмите с собой зонтик, возможен дождь."
        
        return "Зонт не нужен, дождь не ожидается."
    
    except requests.RequestException:
        return "Не удалось получить прогноз погоды."
