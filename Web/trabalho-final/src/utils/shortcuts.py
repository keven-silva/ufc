from typing import Any, Dict

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.settings import settings

templates = Jinja2Templates(directory=str(settings.templates_dir))


def render(
    request: Request,
    template_name: str,
    context: Dict[str, Any] = {},
    status_code: int = 200,
    cookies: Dict[str, Any] = {},
    remove_session: bool = False,
    remove_message: bool = False,
) -> HTMLResponse:
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response: HTMLResponse = HTMLResponse(html_str, status_code=status_code)
    # print(request.cookies)
    response.set_cookie(key="darkmode", value="1")
    if len(cookies.keys()) > 0:
        # set httponly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    if remove_session:
        response.set_cookie(key="session_ended", value="1", httponly=True)
        response.delete_cookie(key="session_id")
    if remove_message:
        response.delete_cookie(key="logged_in")
        response.delete_cookie(key="category")
    return response


def redirect(
    path: str,
    cookies: Dict[str, Any] = {},
    remove_session: bool = False,
) -> RedirectResponse:
    response: RedirectResponse = RedirectResponse(url=path, status_code=302)
    if len(cookies.keys()) > 0:
        # set httponly cookies
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    if remove_session:
        response.set_cookie(key="session_ended", value="1", httponly=True)
        response.delete_cookie(key="session_id")
    return response


def is_htmx(request: Request) -> bool:
    # Cenaŕio onde a requisição é feita via HTMX
    return request.headers.get("hx-request") == "true"
