from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

app = FastAPI()


@app.get("")
def main():
    return "Ok"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
