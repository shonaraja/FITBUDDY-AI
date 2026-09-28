from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import (
    delete_user, get_all_plans, get_all_users, get_plan, get_user,
    save_plan, save_user, update_plan
)
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def _context(request: Request, **kwargs):
    return {"request": request, **kwargs}

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", _context(request))

@router.post("/generate-workout")
def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        user = UserInput(
            name=name, user_id=user_id, age=age, weight=weight,
            goal=goal, intensity=intensity
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            _context(request, error=f"Please check your inputs: {exc}"),
            status_code=400,
        )

    workout_plan = generate_workout_gemini(
        user.name, user.age, user.weight, user.goal, user.intensity
    )
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    save_user(user.model_dump())
    save_plan(user.user_id, workout_plan, nutrition_tip)

    return templates.TemplateResponse(
        "result.html",
        _context(
            request,
            user=user.model_dump(),
            workout_plan=workout_plan,
            nutrition_tip=nutrition_tip,
            updated_plan=None,
            message=None,
        ),
    )

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    user = get_user(data.user_id)
    plan = get_plan(data.user_id)
    if not user or not plan:
        raise HTTPException(status_code=404, detail="User ID not found.")

    revised = update_workout_plan(plan.original_plan, data.feedback)
    tip = generate_nutrition_tip_with_flash(user.goal)
    update_plan(data.user_id, revised, data.feedback, tip)

    user_data = {
        "user_id": user.user_id,
        "name": user.name,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
    }
    return templates.TemplateResponse(
        "result.html",
        _context(
            request,
            user=user_data,
            workout_plan=plan.original_plan,
            nutrition_tip=tip,
            updated_plan=revised,
            message="Your plan has been updated using your feedback.",
        ),
    )

@router.get("/view-all-users")
def view_all_users(request: Request):
    users = get_all_users()
    plans = {p.user_id: p for p in get_all_plans()}
    return templates.TemplateResponse(
        "all_users.html",
        _context(request, users=users, plans=plans),
    )

@router.post("/delete-user/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse("/view-all-users", status_code=303)

# Simple JSON/API endpoints for testing in /docs.
@router.get("/api/users/{user_id}")
def api_get_user(user_id: str):
    user = get_user(user_id)
    plan = get_plan(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
        },
        "plan": None if not plan else {
            "original_plan": plan.original_plan,
            "updated_plan": plan.updated_plan,
            "nutrition_tip": plan.nutrition_tip,
            "feedback": plan.feedback,
        },
    }

@router.get("/api/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}

@router.get("/api/config")
def config_status():
    from .config import AI_ENABLED, GEMINI_WORKOUT_MODEL, GEMINI_TIP_MODEL
    return {
        "ai_enabled": AI_ENABLED,
        "workout_model": GEMINI_WORKOUT_MODEL,
        "tip_model": GEMINI_TIP_MODEL,
    }
