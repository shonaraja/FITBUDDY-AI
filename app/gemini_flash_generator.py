from .config import AI_ENABLED, GEMINI_TIP_MODEL
from .gemini_client import generate_text

def generate_nutrition_tip_with_flash(goal: str) -> str:
    if not AI_ENABLED:
        tips = {
            "weight loss": "Build meals around vegetables, a protein source, whole-food carbohydrates and healthy fats. Stay hydrated and avoid extreme calorie restriction.",
            "muscle gain": "Include a protein-rich food in regular meals, eat enough overall food to support training, and prioritize hydration and sleep.",
            "general wellness": "Aim for balanced meals with vegetables or fruit, protein, whole grains and healthy fats, alongside regular hydration.",
            "flexibility": "Support recovery with adequate fluids and balanced meals containing protein, fruits/vegetables and whole-food carbohydrates.",
        }
        return tips.get(goal, "Choose balanced meals, stay hydrated and prioritize recovery.")

    prompt = f"""
You are FitBuddy's nutrition and recovery assistant.
Give one concise, practical nutrition or recovery tip for a user whose fitness goal is: {goal}.
Keep it to 3–5 sentences. Avoid medical diagnosis, supplements as treatment, extreme dieting,
or guaranteed results. Prefer ordinary foods, hydration, sleep and sustainable habits.
"""
    return generate_text(prompt, GEMINI_TIP_MODEL, temperature=0.4, max_output_tokens=500)
