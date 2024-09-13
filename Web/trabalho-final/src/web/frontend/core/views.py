from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from src.utils.shortcuts import render, is_htmx


router = APIRouter()


@router.get("/", response_class=HTMLResponse, tags=["core"])
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


@router.get("/consequences", response_class=HTMLResponse, tags=["core"])
async def get_consequence_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "consequence/page/consequence.html", context={})


@router.get("/preventions", response_class=HTMLResponse, tags=["core"])
async def get_prevention_page(
    request: Request,
) -> HTMLResponse:
    if is_htmx(request):
        return render(request, "prevention/partials/_main-content.html", context={})
    return render(request, "prevention/pages/prevention.html", context={})


@router.get("/testimonials", response_class=HTMLResponse, tags=["core"])
async def get_testimonial_page(
    request: Request,
) -> HTMLResponse:
    return render(request, "testimony/pages/testimony.html", context={})


@router.get(
    "/faq",
    response_class=HTMLResponse,
    tags=["core"],
)
async def get_faq_page(
    request: Request,
) -> HTMLResponse:
    if is_htmx(request):
        return render(request, "faq/partials/_main-content.html", context={})
    return render(request, "faq/pages/faq.html", context={})
