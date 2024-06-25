import uvicorn
from os import getenv
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'hello': 'world'}

if __name__ == '__main__':
    port = int(getenv('PORT', 8000))
    uvicorn.run("main:app", host='0.0.0.0', port=port)
    # uvicorn.run("backend:fast", host='0.0.0.0', port=port)