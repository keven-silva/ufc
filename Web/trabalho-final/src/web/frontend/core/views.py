from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from src.utils.shortcuts import render


router = APIRouter()


@router.get("/problem", response_class=HTMLResponse, tags=["core"])
async def get_problem_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "global/pages/problem.html", context={})
