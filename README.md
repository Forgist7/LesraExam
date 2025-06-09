# Проект Flask API

Это API на основе Flask с настройкой CI/CD через Jenkins и Docker. Приложение предоставляет эндпоинты для отправки и получения оценок пользователей.

## Требования
- Python 3.12+
- Docker и Docker Compose
- Jenkins (для CI/CD)
- Git

## Локальная настройка и запуск проекта

1. **Клонирование репозитория**
   - Создайте директорию для вашего проекта (если она еще не создана) и перейдите в нее
     ```bash
     mkdir my_project
     cd my_project
     ```
   - Клонируйте репозиторий в вашу директорию
     ```bash
     git clone https://github.com/Forgist7/LestaExam.git
     ```

3. **Настройка переменных окружения**
   - Обновите `.env.example` с вашими настройками или используйте переменные по умолчанию
     ```
     mv .env.example .env
     ```
  
4. **Запуск с помощью Docker Compose**
   - Соберите и запустите приложение:
     ```bash
     docker-compose up -d --build
     ```
   - API будет доступен по адресу `http://localhost:<ПОРТ>` (порт по умолчанию — 6000)

## Настройка Jenkins

1. **Установка Jenkins**
   - Следуйте официальному руководству по установке Jenkins: https://www.jenkins.io/doc/book/installing/
   - Убедитесь, что Docker установлен на сервере Jenkins
   - Добавьте агента Jenkins

2. **Настройка Jenkins Pipeline**
   - Создайте новую задачу типа Pipeline в Jenkins
   - Укажите путь к `Jenkinsfile` в репозитории
   - Запустите pipeline для сборки, тестирования и деплоя приложения

## Процесс CI/CD

Pipeline, определенный в `Jenkinsfile`, включает следующие этапы:

- **Checkout**: Получение исходного кода из репозитория через `checkout scm`
- **Build**: Сборка Docker-образа
- **Test/Lint**: Запуск линтера `flake8` для проверки кода
- **Login to Docker Hub**: Аутентификация в Docker Hub с использованием учетных данных, сохраненных в Jenkins (`docker-hub-creds`)
- **Push**: Отправка собранного Docker-образа в Docker Hub
- **Deploy**:
  - Копирование необходимых файлов в целевую директорию на хосте
  - Остановка существующих контейнеров `docker compose down`, обновление образов `docker compose pull` и запуск приложения `docker compose up -d --build`

Pipeline запускается при каждом push в репозиторий

## Конечные точки API

API доступен по адресу `37.9.53.90:6000/results`

### 1. Проверка доступности
- **GET** `/ping`
  - Проверяет, работает ли API.
  - Пример:
    ```bash
    curl http://localhost:6000/ping
    ```
  - Ответ:
    ```json
    {"status": "pong"}
    ```

### 2. Отправка оценки
- **POST** `/submit`
  - Отправляет имя и оценку пользователя.
  - Пример:
    ```bash
    curl -X POST http://localhost:6000/submit \
      -H "Content-Type: application/json" \
      -d '{"name": "Kirill", "score": 88}'
    ```
  - Ответ:
    ```json
    {"message":"Record added successfully"}
    ```

### 3. Получение результатов
- **GET** `/results`
  - Возвращает все отправленные оценки.
  - Пример:
    ```bash
    curl http://localhost:6000/results
    ```
  - Ответ:
    ```json
    [
      {"id": 1, "name": "Kirill", "score": 88, "timestamp": "2025-05-30T10:25:43"},
      {"id": 2, "name": "Roman", "score": 92, "timestamp": "2025-05-30T10:25:43"}
    ]
    ```
