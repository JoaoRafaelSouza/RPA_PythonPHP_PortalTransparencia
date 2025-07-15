from fastapi import FastAPI
import uvicorn
from controllers import buscar_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o controller com prefixo /api
app.include_router(buscar_controller.router, prefix="/api")

# Rota de verificação
@app.get("/")
def root():
    return {"message": "API funcionando!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)