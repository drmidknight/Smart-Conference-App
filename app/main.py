import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api_routes.api import router as api_router
from utils.config import settings
from inspect import re
from fastapi.openapi.utils import get_openapi



app = FastAPI(docs_url="/", title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)



#origins = ["http://localhost:4300", "http://localhost:4200"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    
    return {"Home Page": "WELCOME TO SMART CONFERENCE APP"}



from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
import shutil
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("uploadfile.html", {"request": request})

 
app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=2020, log_level="info", reload = True)
    print("running")