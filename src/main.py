import uuid

from src.models import UserCreate, UserLogin, TaskCreate, TaskUpdate
from src.service import register_user, login_user, get_tasks, get_task_by_id, update_task, delete_task, create_task


def main():
    suffix = uuid.uuid4().hex[:8]
    # suffix = 'michael'
    username = f"user_{suffix}"
    password = f"pass_{suffix}"
    email = f"{username}@example.com"

    user = UserCreate(username=username, password=password, email=email)

    register_user(user)
    token = login_user(UserLogin(username=user.username, password=user.password))

    # Создание задачи
    task = TaskCreate(title="Начальная задача", description="Первое описание")
    task_id = create_task(token, task)

    # Получение всех задач
    get_tasks(token)

    # Получение конкретной задачи
    get_task_by_id(token, task_id)

    # Обновление задачи
    task_update = TaskUpdate(title="Обновлённый заголовок", description="Новое описание")
    update_task(token, task_id, task_update)

    # Удаление задачи
    delete_task(token, task_id)

    # Проверка, что задача удалена
    print("\n🚨 Попытка получить удалённую задачу:")
    get_task_by_id(token, task_id)

    print('\n\n✅Проверка завершена, системы работает')


if __name__ == "__main__":
    main()