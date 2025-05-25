import requests
from pydantic import ValidationError

from models import UserCreate, UserLogin, TaskCreate, TaskUpdate, UserResponse, Task
from src.models import Token

API_BASE_URL = "http://212.57.118.30:8000/"
API_USER_URL = f"{API_BASE_URL}/api/v1/user/"
API_TASKS_URL = f"{API_BASE_URL}/api/v1/tasks/"


def validate_response(data: str, model):
    try:
        model(**data)
    except ValidationError:
        raise ValueError("❌ Возвращены данные неверного формата")


def register_user(user: UserCreate):
    url = f"{API_USER_URL}register/"
    response = requests.post(url, json=user.model_dump())

    if response.status_code == 200:
        validate_response(response.json(), UserResponse)
        user_data = UserResponse(**response.json())
        print(f"✅ Пользователь '{user_data.username}' зарегистрирован")

    elif response.status_code == 409:
        print("⚠️ Пользователь уже существует")

    else:
        raise (f"❌ Ошибка регистрации: {response.status_code} — {response.text}")


def login_user(credentials: UserLogin) -> Token:
    url = f"{API_USER_URL}login/"
    response = requests.post(url, json=credentials.model_dump())

    if response.status_code == 200:
        validate_response(response.json(), Token)
        print("🔐 Вход выполнен")
        return response.json()["token"]

    else:
        raise (f"❌ Ошибка входа: {response.status_code} — {response.text}")


def get_user(token: str):
    url = f"{API_USER_URL}profile/"
    headers = {"Authorization": f"{token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        validate_response(response.json(), UserResponse)
        print(f"🔎 Текущий пользователь - {response.json()['username']}\n")

    else:
        raise (f"❌ Текущий пользователь не распознан")


def create_task(token: str, task: TaskCreate) -> int:
    url = f"{API_TASKS_URL}"
    headers = {"Authorization": f"{token}"}
    response = requests.post(url, headers=headers, json=task.model_dump())

    if response.status_code == 200:
        validate_response(response.json(), Task)
        task_data = response.json()
        print(f"📝 Задача №'{task_data['id']}' создана")
        return task_data["id"]

    else:
        raise (f"❌ Ошибка создания задачи: {response.status_code} — {response.text}")


def get_tasks(token: str):
    url = f"{API_TASKS_URL}"
    headers = {"Authorization": f"{token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"📋 Все задачи: {response.json()}")

    else:
        print(f"❌ Ошибка получения задач: {response.status_code} — {response.text}")


def get_task_by_id(token: str, task_id: int):
    url = f"{API_TASKS_URL}{task_id}"
    headers = {"Authorization": f"{token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        validate_response(response.json(), Task)
        print(f"🔎 Задача по ID {task_id} найдена")

    else:
        print(f"❌ Ошибка получения задачи по ID {task_id}")


def update_task(token: str, task_id: int, task_update: TaskUpdate):
    url = f"{API_TASKS_URL}{task_id}"
    headers = {"Authorization": f"{token}"}
    response = requests.patch(url, headers=headers, json=task_update.model_dump())

    if response.status_code == 200:
        validate_response(response.json(), Task)
        print(f"✏️ Задача {task_id} обновлена")

    else:
        print(f"❌ Ошибка обновления задачи {task_id}")


def delete_task(token: str, task_id: int):
    url = f"{API_TASKS_URL}{task_id}"
    headers = {"Authorization": f"{token}"}
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        if isinstance(response.json(), str):
            raise ("❌ Возвращены данные неверного формата")

        print(f"🗑️ Задача {task_id} удалена")

    else:
        print(f"❌ Ошибка удаления задачи: {response.status_code} — {response.text}")
