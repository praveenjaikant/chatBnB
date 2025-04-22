import uvicorn
from mcp_setup import main
from pydantic import BaseModel

from dotenv import load_dotenv
from fastapi import FastAPI, Body

load_dotenv(override=True)

class MessageRequest(BaseModel):
    message: str


app = FastAPI()

@app.post("/")
async def read_root(payload: MessageRequest = Body(...)):
   return await main(message=payload.message)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8080)