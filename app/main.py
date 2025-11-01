import uvicorn
from fastapi import FastAPI
from app.db.database import engine, Base, Session
from app.router import router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal API")

app.include_router(router.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
