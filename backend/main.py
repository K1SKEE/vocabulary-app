import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.auth_handlers import register_router, login_router
from api.user_handlers import user_router

app = FastAPI(title="vocabulary-app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

main_api_router = APIRouter(prefix="/api/v1")

main_api_router.include_router(register_router, prefix='/register',
                               tags=['register'])
main_api_router.include_router(login_router, prefix="/token", tags=["token"])
main_api_router.include_router(user_router, prefix='/user', tags=["user"])

app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
