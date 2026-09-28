from .config import AI_ENABLED, GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text

def update_workout_plan(original_plan: str, feedback: str) -> str:
    if not AI_ENABLED:
        return original_plan + f"""

UPDATED BY USER FEEDBACK
Feedback: {feedback}

Testing mode note:
Gemini is not configured, so the original plan is retained. Add GEMINI_API_KEY
to .env and restart the server to enable AI-based plan regeneration.
"""

    prompt = f"""
You are FitBuddy. Revise the workout plan below using the user's feedback.

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a complete revised 7-day plan, not only the changed lines.
Keep the original useful structure, clearly show each day, warm-up, main workout,
cooldown/recovery, and include a safety note. Apply the feedback where reasonable.
Do not diagnose medical conditions or make guaranteed health claims.
"""
    return generate_text(prompt, GEMINI_WORKOUT_MODEL, temperature=0.6, max_output_tokens=5000)
