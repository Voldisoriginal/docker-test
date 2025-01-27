from fastapi import FastAPI
from pydantic import BaseModel
import httpx
app = FastAPI()

class FieldResponse(BaseModel):
    Name: str
    Description: str

@app.get("/fields", response_model=FieldResponse)
def get_fields():
    return {
        "Name": "Пример Имени",
        "Description": "Пример Описания"
    }

class Task(BaseModel):
    Id: int
    ServiceName: str
    Name: str
    Description: str
    Color:str


@app.post("/submit")
async def submit_task(field: FieldResponse):
    print(f"Получены данные: {field}")

    task = Task(
        Id=1,
        ServiceName="app1 задачи",
        Name=field.Name,
        Description=field.Description,
        Color="red"
    )

    container_address = "http://docker-test-mainapp-1:8000/tasks"
    print(task.dict())
    async with httpx.AsyncClient() as client:
        response = await client.post(container_address, json=task.dict())

        # Добавим проверку кода состояния
        if response.is_success:
            try:
                response_data = response.json()
            except Exception as e:
                print("Ошибка при обработке JSON:", str(e))
                raise
        else:
            raise Exception(f"Ошибка при отправке задачи: {response.status_code} - {response.text}")

    return {"message": "Данные получены и отправлены", "data": response_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)