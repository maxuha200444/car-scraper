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
        count_elem = soup.find(string=lambda t: t and 'Sõidukit kokku' in t)
        if count_elem:
            parent = count_elem.parent
            text = parent.get_text(strip=True) if parent else count_elem
            numbers = re.findall(r'\d+', text)
            if numbers:
                return int(numbers[0].replace(' ', ''))
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def update_history():
    count = get_car_count()
    if count is None:
        print("Не удалось получить число. Пропускаем.")
        return
    now = datetime.now()
    new_row = pd.DataFrame({
        'timestamp': [now.strftime('%Y-%m-%d %H:%M:%S')],
        'date': [now.strftime('%Y-%m-%d')],
        'car_count': [count]
    })
    filename = 'car_count_history.csv'
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Сохранено: {count} авто на {now}")

if __name__ == "__main__":
    update_history()
