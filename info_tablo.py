import tkinter as tk
from news import fetch_news, display_news, refresh_news
from zont import get_weather
from PIL import Image, ImageTk
import webbrowser

def open_link(url):
    webbrowser.open(url)

# Создание основного окна
root = tk.Tk()
root.title("Информационное табло")
root.geometry("1024x768")

# Установка зеленого фона
root.configure(bg='#90ee90')

# Создание верхней рамки для заголовка
top_frame = tk.Frame(root, bg='darkgreen', height=50)
top_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

# Добавление заголовка
label = tk.Label(top_frame, text="Информационное табло ver. 1.0", bg='darkgreen', fg='white', font=('Arial', 16))
label.pack(pady=10)

# Настройка сетки для равного распределения колонок
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Глобальная переменная для метки изображения
image_label = None

# Функция для отображения прогноза погоды
def display_weather():
    lat = 55.668856
    lon = 37.587585
    weather_info = get_weather(lat, lon)  # Получаем прогноз погоды
    weather_label.config(text=weather_info)  # Обновляем текст метки с погодой

    # Обновление изображения в зависимости от прогноза погоды
    if "не" in weather_info:
        show_image("no_zont.jpg")  # Если дождь, показываем "нужен зонт"
    else:
        show_image("yes_zond.jpg")  # Если нет дождя, показываем "не нужен зонт"
        
    root.after(180000, display_weather)  # Устанавливаем повторный вызов через 3 минуты (180000 мс)

# Функция для отображения изображения
def show_image(image_path):
    global image_label  # Указываем, что мы используем глобальную переменную
    try:
        img = Image.open(image_path)  # Открываем изображение
        img = img.resize((200, 200), Image.LANCZOS)  # Изменяем размер изображения
        img_tk = ImageTk.PhotoImage(img)  # Преобразуем в PhotoImage для Tkinter

        # Если изображение уже существует, просто обновляем его
        if image_label is not None:
            image_label.config(image=img_tk)
            image_label.image = img_tk  # Сохраняем ссылку на изображение
        else:
            image_label = tk.Label(root, image=img_tk, bg='#90ee90')
            image_label.grid(row=3, column=0, columnspan=3)  # Размещаем изображение под новостями (строка 3)
            image_label.image = img_tk  # Сохраняем ссылку на изображение
            
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

# Создание метки для прогноза погоды
weather_label = tk.Label(root, bg='#90ee90', fg='black', font=('Arial', 14), wraplength=600)
weather_label.grid(row=2, column=0, columnspan=3, pady=20)  # Размещаем метку под новостями

# Начальная загрузка данных о погоде
display_weather()

# Отображение новостей и установка обновления каждую минуту
refresh_news(root, open_link)

# Запуск основного цикла
root.mainloop()
