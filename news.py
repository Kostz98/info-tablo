import feedparser
import re
import tkinter as tk
from tkinter import messagebox

# Глобальная переменная для отслеживания текущей позиции
current_index = 0

def fetch_news():
    rss_url = "https://www.anekdot.ru/rss/export_j.xml"
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries:  # Получение всех анекдотов
        title = entry.title
        link = entry.link if isinstance(entry.link, str) else entry.links[0].href
        description = re.sub(r'<[^>]+>', '', entry.description)  # Удаляем HTML-теги

        # Добавляем каждый анекдот в список
        news_items.append((title, link, description))
    
    return news_items

def display_news(root, open_link_callback):
    global current_index
    news_items = fetch_news()
    num_news = len(news_items)
    
    # Очистка старых новостей
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) == 1:
            widget.destroy()

    # Отображаем три новости начиная с current_index
    for index in range(3):
        item_index = (current_index + index) % num_news  # Обеспечиваем круговое обновление
        title, link, description = news_items[item_index]
        
        news_frame = tk.Frame(root, bg='#e0ffe0', padx=10, pady=10, bd=2, relief=tk.RAISED, width=250)
        news_frame.grid(row=1, column=index, padx=5, pady=5, sticky='nsew')
        news_frame.grid_propagate(False)

        # Настройка заголовка и описания с wraplength
        title_label = tk.Label(news_frame, text=title, fg='blue', cursor="hand2", bg='#e0ffe0', font=('Arial', 14),
                               wraplength=220, justify='left')
        title_label.pack(anchor='n', fill='both', expand=True)

        description_label = tk.Label(news_frame, text=description, bg='#e0ffe0', wraplength=220, justify='left')
        description_label.pack(anchor='n', fill='both', expand=True)

        # Привязка открытия ссылки
        title_label.bind("<Button-1>", lambda e, url=link: open_link_callback(url))

    # Увеличиваем current_index на 3, чтобы показать следующие новости в следующий раз
    current_index = (current_index + 3) % num_news  # Обеспечиваем круговое обновление

def open_link(url):
    import webbrowser
    webbrowser.open(url)

def refresh_news(root, open_link_callback):
    display_news(root, open_link_callback)
    root.after(60000, refresh_news, root, open_link_callback)  # Обновляем каждую минуту (60000 мс)
