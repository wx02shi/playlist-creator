from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()
load_dotenv()


@app.get("/")
def health():
    return "Healthy"
