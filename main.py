from fastapi import FastAPI
from pydantic import BaseModel


from fastapi import FastAPI
from apps.users import router as auth_router
import uvicorn

app = FastAPI()
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
