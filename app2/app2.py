from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/container_name")
async def get_container_name():
    # Получаем имя хоста (в Docker это обычно ID или имя контейнера)
    container_name = socket.gethostname()
    return {"container_name": container_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)