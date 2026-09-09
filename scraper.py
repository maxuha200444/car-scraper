import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
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
        print("⚠️ Не найдено 'Sõidukit kokku' на странице.")
        return None
    except Exception as e:
        print(f"❌ Ошибка при запросе: {e}")
        return None

def update_history():
    count = get_car_count()
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    date_only = now.strftime('%Y-%m-%d')
    # Записываем число или 'Ошибка'
    count_str = str(count) if count is not None else 'Ошибка'
    
    filename = 'car_count_history.csv'
    file_exists = os.path.isfile(filename)
    
    # Открываем файл для добавления (создаём, если нет)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Если файл новый – пишем заголовок
        if not file_exists:
            writer.writerow(['timestamp', 'date', 'car_count'])
        writer.writerow([timestamp, date_only, count_str])
    
    print(f"✅ Данные сохранены: {count_str} на {timestamp}")

if __name__ == "__main__":
    update_history()
