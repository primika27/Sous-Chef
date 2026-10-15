from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.recipes.router import router as recipe_router

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        recipe_router, 
        prefix=f"{settings.API_V1_PREFIX}/recipes", 
        tags=["Recipes"]
    )
    return app

app = create_application()