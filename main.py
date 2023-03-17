import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI(title="vocabulary-app")

main_api_router = APIRouter()

app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
