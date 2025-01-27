from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import docker
import httpx

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Позволяет запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Позволяет все методы
    allow_headers=["*"],  # Позволяет все заголовки
)

client = docker.from_env()
tasks = []  # Простейшая база данных в памяти


class Task(BaseModel):
    Id: int
    ServiceName: str
    Name: str
    Description: str
    Color: str


async def get_container_api_address(container_name: str) -> str:
    """Получает адрес API конкретного контейнера по имени."""
    try:
        container = client.containers.get(container_name)
        ports = container.attrs['NetworkSettings']['Ports']
        host_port = None

        # Находим доступный хост-порт
        for port, bindings in ports.items():
            if bindings:
                host_port = bindings[0]['HostPort']
                break

        if host_port is None:
            return None  # Если хост-порт не найден, возвращаем None

        return f"http://{container.name}:{host_port}"

    except docker.errors.NotFound:
        return None  # Контейнер не найден


@app.post("/submit_task")
async def submit_task(task: dict):
    print(task)  # Выводим полученные данные

    # Извлекаем имя контейнера из задачи
    container_name = task.pop('containerName', None)  # Убираем имя контейнера из task

    if container_name is None:
        return {"error": "Имя контейнера не указано"}

    container_address = await get_container_api_address(container_name)  # Получение адреса по имени контейнера
    if container_address is None:
        return {"error": "Контейнер не найден или нет доступного порта"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{container_address}/submit", json=task)
        response_data = response.json()

        if response.status_code == 200:
            return {"message": "Данные успешно отправлены", "data": response_data['data']}
        else:
            return {"error": response_data}



@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    print(Task)
    tasks.append(task)
    return task


@app.get("/services")
def get_services():
    """Возвращает список всех запущенных Docker-контейнерах"""
    containers = client.containers.list()
    services = []
    for container in containers:
        services.append({
            'id': container.id,
            'name': container.name,
            'status': container.status,
            'image': container.image.tags[0] if container.image.tags else "N/A",
            'ports': container.attrs['NetworkSettings']['Ports'],
            'address': f"http://{container.attrs['NetworkSettings']['IPAddress']}:" + (
                next(iter(container.attrs['NetworkSettings']['Ports'].keys()), 'N/A') if
                container.attrs['NetworkSettings']['Ports'] else "N/A"),
        })
    return services


@app.get("/getapi/{container_name}")
async def get_api(container_name: str):
    """Запрашивает API конкретного контейнера по имени и возвращает ответ"""
    address = await get_container_api_address(container_name)  # Используем новую функцию
    if address is None:
        return {"error": f"Контейнер с именем {container_name} не найден или нет доступного порта"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{address}/fields")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {str(e)}")
            return {"error": str(e)}
        except httpx.HTTPStatusError as e:
            print(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error occurred: {e}"}

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
