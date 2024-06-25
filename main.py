import uvicorn
from os import getenv

if __name__ == '__main__':
    port = int(getenv('PORT', 8080))
    uvicorn.run("backend:fast", host='0.0.0.0', port=port)
    # uvicorn.run("main:app", host='0.0.0.0', port=port)