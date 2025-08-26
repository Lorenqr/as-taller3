from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .routes import users

# TODO: Crear la instancia de FastAPI
app = FastAPI(title="Tienda Virtual API", version="1.0.0")

# TODO: Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# TODO: Incluir los routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(carts.router, prefix="/api/v1/carts", tags=["carts"])

@app.get("/")
async def root():
    return {"message": "Tienda Virtual API"}


    # TODO: Endpoint de verificación de salud
@app.get("/health", tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        # Intentar ejecutar una consulta simple para verificar DB
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "database": "disconnected", "error": str(e)}
        )