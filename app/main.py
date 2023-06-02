import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api_routes.api import router as api_router
from inspect import re
from fastapi.openapi.utils import get_openapi



app = FastAPI(docs_url="/")



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


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host='http://dev-1.aiti-kace.com.gh', port=8000, log_level="info",workers=4, reload = True)
    print("running")