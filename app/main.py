from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.chat.router import router as chat_router
from app.exceptions import TokenExpiredException, TokenNoFoundException
from app.users.router import router as users_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_origins=["*"],
    allow_credentials=True,
    # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_methods=["*"],
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(users_router)
app.include_router(chat_router)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(
    request: Request,
    exc: HTTPException
):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(
    request: Request,
    exc: HTTPException
):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")
