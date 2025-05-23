# Импортируем библиотеку httpx для HTTP-запросов
import httpx

# Создаем данные для авторизации (email и пароль)
payload = {
    "email": "test@gmail.com",
    "password": "123456"
}

# Отправляем POST-запрос на эндпоинт для входа в систему
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload)

# Получаем JSON-ответ от сервера
login_response_data = login_response.json()

# Выводим статус код ответа
print(login_response.status_code)

# Выводим содержимое ответа от сервера (обычно содержит токены доступа)
print(login_response_data)

# Извлекаем access token из ответа сервера
ACCESS_TOKEN = login_response_data["token"]["accessToken"]

# Формируем заголовки для последующих запросов, добавляя токен в Authorization
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Отправляем GET-запрос для получения информации о текущем пользователе
user_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)

# Выводим статус код ответа
print(user_me_response.status_code)

# Выводим информацию о текущем пользователе
print(user_me_response.json())