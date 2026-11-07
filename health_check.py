import sys
import requests

url = "http://localhost:5000/health"
timeout = 3

try:
    response = requests.get(url, timeout=timeout)
    if response.status_code == 200:
        print("Сервіс успішно пройшов перевірку healthcheck!")
        sys.exit(0)
    else:
        print(f"Помилка: {response.status_code}")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Сервіс недоступний: {e}")
    sys.exit(1)