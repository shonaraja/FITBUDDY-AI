# FitBuddy – AI Fitness Plan Generator

FitBuddy is based on the supplied project documentation: FastAPI + Jinja2 frontend, SQLite/SQLAlchemy persistence, Gemini-powered workout generation, nutrition/recovery tips, feedback-based plan updates, an admin view, and API documentation.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   └── routes.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── all_users.html
├── static/css/style.css
├── tests/test_app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

## 1. Open in VS Code

Extract the ZIP, open the `FitBuddy` folder in VS Code, then open Terminal → New Terminal.

## 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Copy `.env.example` to `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and put your Gemini API key after `GEMINI_API_KEY=`.

The app reads the current Gemini SDK through `google-genai`. The model names are configurable so you can change them without modifying application code.

If no API key is supplied, FitBuddy still starts in local demo mode and returns a deterministic test plan. This is useful for checking the frontend, database, routes and forms before adding the API key.

## 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open:

- Home: http://127.0.0.1:8000
- Admin dashboard: http://127.0.0.1:8000/view-all-users
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

## 6. Test the complete project

Run:

```bash
pytest
```

The tests exercise the homepage, health endpoint, plan generation in demo mode, database storage and retrieval.

## 7. Test the main workflow manually

1. Open the home page.
2. Enter Name, User ID, Age, Weight, Goal and Intensity.
3. Click **Generate 7-Day Plan**.
4. Confirm the plan and nutrition/recovery tip appear.
5. Enter feedback such as `include more cardio and one additional rest day`.
6. Click **Update Plan with AI**.
7. Open **Admin** and verify both original and updated plans.
8. Open **API Docs** to test the JSON endpoints.

## Important safety note

FitBuddy is an educational/demo fitness-planning application. AI-generated workout and nutrition suggestions are not medical advice. Users with injuries, medical conditions, pregnancy, or other special circumstances should seek appropriate professional guidance before following an exercise or nutrition program.

## Why this version differs from the supplied document

The supplied documentation describes Gemini 1.5 Pro and Gemini Flash and the older `google-generativeai` SDK. The implementation keeps the same project functions and architecture, but uses Google's current `google-genai` Python SDK and configurable model names so the application is maintainable as Gemini model availability changes.
