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
        
        # Получаем весь текст страницы
        page_text = soup.get_text()
        # Ищем число, за которым следует слово sõidukit или autot или kokku
        # Например: "15 724 sõidukit" или "15 724 autot" или "sõidukit 15 724"
        patterns = [
            r'(\d{1,3}(?:\s?\d{3})*)\s*sõidukit',  # число, пробел, sõidukit
            r'(\d{1,3}(?:\s?\d{3})*)\s*autot',      # число, пробел, autot
            r'sõidukit\s*(\d{1,3}(?:\s?\d{3})*)',   # sõidukit, пробел, число
            r'kokku\s*(\d{1,3}(?:\s?\d{3})*)',      # kokku, пробел, число
        ]
        for pattern in patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                num_str = match.group(1).replace(' ', '')
                if num_str.isdigit():
                    return int(num_str)
        # Если не нашли, пробуем найти все числа и взять самое большое (запасной вариант)
        all_numbers = re.findall(r'(\d{1,3}(?:\s?\d{3})*)', page_text)
        numbers = [int(n.replace(' ', '')) for n in all_numbers if n.replace(' ', '').isdigit()]
        if numbers:
            # Берём самое большое, если оно больше 1000 (отсекаем мелкие числа)
            max_num = max(numbers)
            if max_num > 1000:
                return max_num
        return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def update_history():
    count = get_car_count()
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    date_only = now.strftime('%Y-%m-%d')
    count_str = str(count) if count is not None else 'Ошибка'
    
    filename = 'car_count_history.csv'
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'date', 'car_count'])
        writer.writerow([timestamp, date_only, count_str])
    
    print(f"✅ Сохранено: {count_str} на {timestamp}")

if __name__ == "__main__":
    update_history()
