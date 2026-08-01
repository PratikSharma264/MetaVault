# MetaVault

Mobile-first fitness and calorie tracking built with Django REST Framework and a polished vanilla web interface.

## Run locally

1. Install Python 3.11+ and create a virtual environment.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`. Add `OPENAI_API_KEY` to enable live food estimates and coaching.
4. `python manage.py migrate`
5. `python manage.py runserver`

Open `http://127.0.0.1:8000`. The AI endpoints stay useful without an API key by returning safe local estimates and goal-aware coaching prompts.
