import uvicorn 
from fastapi import FastAPI ,File, UploadFile ,Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from routes import routes



app = FastAPI()


app.include_router(routes)


if __name__ == "__main__":
    uvicorn.run("server:app", reload=True, host="0.0.0.0", port=8000)
