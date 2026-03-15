from fastapi import FastAPI, Depends # Add Depends
from fastapi.middleware.cors import CORSMiddleware

# import routers
from app.routers import loads, carriers, negotiation, metrics, call_analysis
from app.security import get_api_key # Import the new dependency

def create_app() -> FastAPI:
    app = FastAPI(
        title="HappyRobot Carrier Sales API",
        description="Backend API for automated inbound carrier sales",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Apply the security dependency to all routers globally
    # This fulfills the "all endpoints" requirement
    app.include_router(loads.router, dependencies=[Depends(get_api_key)])
    app.include_router(carriers.router, dependencies=[Depends(get_api_key)])
    app.include_router(negotiation.router, dependencies=[Depends(get_api_key)])
    app.include_router(metrics.router, dependencies=[Depends(get_api_key)])
    app.include_router(call_analysis.router, dependencies=[Depends(get_api_key)])

    @app.get("/")
    def health_check():
        return {
            "status": "running",
            "service": "happyrobot-backend"
        }

    return app

app = create_app()