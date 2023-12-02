import os
from contextlib import asynccontextmanager

import dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from telethon import TelegramClient, errors

dotenv.load_dotenv()

# Use your own values from my.telegram.org
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
client = TelegramClient("anon", api_id, api_hash)


app = FastAPI(
    title="Telegram Message Sender",
    # description=RELEASE_NOTE,
    summary="Send messages to Telethon library",
    version="V1.0.0 - send message",
    contact={
        "name": "Mahdi Kiani",
        "email": "mahdikiany@gmail.com",
    },
    # openapi_tags=tags_metadata,
)


class BaseHTTPException(Exception):
    def __init__(self, status_code: int, error: str, message: str):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(message)


@app.exception_handler(BaseHTTPException)
async def base_http_exception_handler(request: Request, exc: BaseHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error": exc.error},
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}


class LoginDetail(BaseModel):
    phone: str
    code: str | None = None
    password: str | None = None


@app.post("/get_code")
async def get_code(login_detail: LoginDetail):
    await client.connect()
    await client.send_code_request(login_detail.phone)
    return {"status": "code sent"}


@app.post("/login")
async def login(login_detail: LoginDetail):
    try:
        await client.connect()
    except ValueError as e:
        client = TelegramClient("anon", api_id, api_hash)
        await client.connect()

    me = await client.get_me()
    if not me:
        two_step_detected = False
        try:
            me = await client.sign_in(login_detail.phone, code=login_detail.code)
        except errors.SessionPasswordNeededError:
            two_step_detected = True
        except (
            errors.PhoneCodeEmptyError,
            errors.PhoneCodeExpiredError,
            errors.PhoneCodeHashEmptyError,
            errors.PhoneCodeInvalidError,
        ):
            raise BaseHTTPException(
                status_code=400, error="login failed", message="code is invalid"
            )
        except Exception as e:
            raise BaseHTTPException(
                status_code=400, error="login failed", message=str(e)
            )

        if two_step_detected:
            try:
                me = await client.sign_in(
                    phone=login_detail.phone, password=login_detail.password
                )
            except Exception as e:
                raise BaseHTTPException(
                    status_code=400, error="login failed", message=str(e)
                )

    return {"status": f"logged in with {me}"}


@app.get("/logout")
async def logout(request: Request):
    await client.log_out()
    return {"status": "logged out"}


class Message(BaseModel):
    phone: str
    message: str


@app.post("/send_message")
async def send_message(msg: Message):
    await client.connect()
    entity = await client.get_entity(msg.phone)
    print(entity)
    await client.send_message(entity, msg.message)
    return {"status": "message sent"}
