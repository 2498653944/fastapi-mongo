from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from routes.student import router as StudentRouter
from routes.admin import router as AdminRouter
from routes.lpldata import router as LplRouter

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware,
                   minimum_size=1000)

token_listener = JWTBearer()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(LplRouter, tags=["lpldata"], prefix="/v1")
