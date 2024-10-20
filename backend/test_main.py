from sqlalchemy.orm import Session
from api.routes.auth_route import auth_router
from fastapi import FastAPI, Depends, HTTPException

import uvicorn


app = FastAPI()

# Zaregistruj routery pre používateľské operácie (registrácia, vytváranie admina)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")

# uvicorn main:app --reload
# uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000