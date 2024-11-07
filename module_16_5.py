from fastapi import FastAPI, status, Body, HTTPException, Request, Form, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    user_id: int = None
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int) -> HTMLResponse:
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})


@app.post("/user/{username}/{age}", response_model=str)
async def create_user(user: User, username: str = Path(min_length=4, max_length=20, description="Enter username", example="John"),
        age: int = Path(ge=18, le=100, description="Enter age", example=44)) -> str:
    if users:
        user_id = max(user.user_id for user in users) + 1
    else:
        user_id = 1
    user.user_id = user_id
    user.username = username
    user.age = age
    users.append(user)
    return f"User {user_id} has been registered"


@app.put("/user/{user_id}/{username}/{age}", response_model=str)
async def update_user(user_id: str=Path(min_length=0, max_length=2000, description="Enter id", example="1"),
                username: str=Path(min_length=5, max_length=20, description="Enter your username", example="UrbanUser"),
                age: int=Path(ge=18, le=100, description="Enter your age", example=44)) -> str:
    up_user = next((user for user in users if user.user_id == user_id), None)
    if up_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    else:
        up_user.username = username
        up_user.age = age
        return f"User {user_id} has been updated."


@app.delete("/user/{user_id}", response_model=str)
async def delete_message(user_id: str=Path(min_length=0, max_length=2000, description="Enter id", example="1")) -> str:
    del_user = next((user for user in users if user.user_id == user_id), None)
    if del_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    else:
        users.remove(del_user)
        return f"User with ID {user_id} has been deleted."