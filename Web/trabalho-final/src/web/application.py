from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
# from src.auth.backends import JWTCookieBackend
from src.logging import configure_logging
from src.settings import settings
from src.web.api.router import api_router
from src.web.frontend.router import frontend_router
from src.web.handlers import register_exceptions_handlers
from src.web.lifetime import register_shutdown_event, register_startup_event

# from starlette.middleware.authentication import AuthenticationMiddleware



def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="bilhetify",
        version=settings.version,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds StaticFiles to the application.
    app.mount(
        "/static",
        StaticFiles(directory=str(settings.static_dir), html=True),
        name="static",
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Adds exception handlers.
    register_exceptions_handlers(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=frontend_router, prefix="")

    # Adds middlewares to the application.
    # app.add_middleware(
    #     middleware_class=AuthenticationMiddleware,
    #     backend=JWTCookieBackend(),
    # )

    return app
