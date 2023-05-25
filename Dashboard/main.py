from fastapi import FastAPI
app = FastAPI()

from fastapi.responses import FileResponse

@app.get("/")
def read_root():
    return FileResponse("index.html")
