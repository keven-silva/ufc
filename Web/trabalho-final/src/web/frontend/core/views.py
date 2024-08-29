from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from src.utils.shortcuts import render


router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse, tags=["core"])
async def get_dashboard_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "dashboard/pages/dashboard.html", context={})


@router.get("/problems", response_class=HTMLResponse, tags=["core"])
async def get_problem_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "problem/pages/problem.html", context={})


@router.get("/causes", response_class=HTMLResponse, tags=["core"])
async def get_cause_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "cause/pages/cause.html", context={})


@router.get("/impacts", response_class=HTMLResponse, tags=["core"])
async def get_impact_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "impact/pages/impact.html", context={})
