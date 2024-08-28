from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from src.utils.shortcuts import is_htmx, render
from starlette.exceptions import HTTPException as StarletteHTTPException


async def not_found_exception_handler(request: Request, exc: Any) -> HTMLResponse:
    if is_htmx(request):
        return JSONResponse({"error": "Page not found"}, status_code=404)
    return render(request, "exception/pages/404.html", status_code=404)


async def server_error_exception_handler(request: Request, exc: Any) -> HTMLResponse:
    if is_htmx(request):
        return JSONResponse({"error": "Internal server error"}, status_code=500)
    return render(request, "exception/pages/500.html", status_code=500)


def register_exceptions_handlers(app: FastAPI) -> None:  # pragma: no cover
    """
    Registers exception handlers.

    :param app: fastAPI application.
    """
    app.add_exception_handler(StarletteHTTPException, not_found_exception_handler)
    app.add_exception_handler(Exception, server_error_exception_handler)
