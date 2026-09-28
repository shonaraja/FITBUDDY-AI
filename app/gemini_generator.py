from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text

def _demo_plan(name: str, goal: str, intensity: str, age: int, weight: float) -> str:
    return f"""FITBUDDY 7-DAY WORKOUT PLAN
User: {name}
Age: {age} | Weight: {weight:g} kg
Goal: {goal.title()} | Intensity: {intensity.title()}

DAY 1 – FULL BODY
Warm-up: 5–10 minutes brisk walking + mobility.
Main workout: Bodyweight squats 3x10, incline push-ups 3x8, glute bridges 3x12, plank 3x20–30 sec.
Cooldown: 5 minutes gentle stretching.

DAY 2 – CARDIO + CORE
Warm-up: 5 minutes easy movement.
Main workout: Brisk walk/cycle 20 minutes, dead bug 3x10/side, bird dog 3x10/side.
Cooldown: Easy walking + stretching.

DAY 3 – LOWER BODY
Warm-up: 5–10 minutes.
Main workout: Squats 3x10, reverse lunges 3x8/side, calf raises 3x15, glute bridge 3x12.
Cooldown: Lower-body stretches.

DAY 4 – RECOVERY
Easy walk 15–20 minutes, mobility, breathing and gentle stretching.

DAY 5 – UPPER BODY + CORE
Warm-up: 5–10 minutes.
Main workout: Incline push-ups 3x8, resistance-band rows 3x12, shoulder raises 3x10, plank 3x20–30 sec.
Cooldown: Upper-body stretching.

DAY 6 – CARDIO + FULL BODY
Warm-up: 5 minutes.
Main workout: 20–30 minutes moderate cardio + 2 rounds of squats, wall push-ups and step-ups.
Cooldown: 5–10 minutes.

DAY 7 – REST / LIGHT MOBILITY
Rest, hydration and gentle stretching.

GENERAL NOTES
• Keep 60–90 seconds rest between strength sets.
• Start comfortably and increase difficulty gradually.
• Stop if you feel sharp pain, dizziness, unusual shortness of breath or feel unwell.
• This demo plan is for application testing and is not medical advice.
"""

def generate_workout_gemini(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    from .config import AI_ENABLED
    if not AI_ENABLED:
        return _demo_plan(name, goal, intensity, age, weight)

    prompt = f"""
You are FitBuddy, a responsible fitness-planning assistant.
Create a personalized 7-day beginner-to-intermediate workout plan.

User:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Return exactly these sections for each day:
DAY N – FOCUS
Warm-up: 5–10 minutes
Main workout: exercise name, sets/reps or duration, and rest
Cooldown/recovery: 1–2 concise suggestions

Requirements:
- Cover all 7 days.
- Respect the requested intensity.
- Include at least one recovery/rest day.
- Do not prescribe medication or diagnose conditions.
- Do not promise a specific amount of weight loss or muscle gain.
- Add a short "Safety note" at the end.
- Keep the response practical and easy to follow.
"""
    return generate_text(prompt, GEMINI_WORKOUT_MODEL, temperature=0.6, max_output_tokens=5000)
