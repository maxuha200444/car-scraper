import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os

def get_car_count():
    url = 'https://autoportaal.ee/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ищем элемент с текстом
        count_elem = soup.find(string=lambda t: t and 'Sõidukit kokku' in t)
        if count_elem:
            parent = count_elem.parent
            text = parent.get_text(strip=True) if parent else count_elem
            numbers = re.findall(r'\d+', text)
            if numbers:
                return int(numbers[0].replace(' ', ''))
        # Если не нашли, пробуем поискать по классу или другому паттерну (для отладки)
        # Например, можно вывести весь текст страницы (но для отладки лучше написать в лог)
        print("Не удалось найти 'Sõidukit kokku'. Проверьте разметку.")
        return None
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None

def update_history():
    count = get_car_count()
    now = datetime.now()
    # Всегда создаём запись, даже если count = None
    new_row = pd.DataFrame({
        'timestamp': [now.strftime('%Y-%m-%d %H:%M:%S')],
        'date': [now.strftime('%Y-%m-%d')],
        'car_count': [count if count is not None else 'Ошибка']
    })
    filename = 'car_count_history.csv'
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Данные сохранены: {count if count is not None else 'Не удалось получить'} на {now}")

if __name__ == "__main__":
    update_history()
