# NutriPlan AI

An AI-powered nutrition tracking and meal planning API. Set macro goals, browse a food database, log daily meals, track calories and macros against your goals, and generate personalized meal plans with Claude AI.

## Tech Stack

- Python, Flask
- SQLAlchemy, SQLite
- Claude AI (Anthropic API)
- JWT Authentication, Bcrypt
- Swagger API Documentation

## Features

- User signup and login with hashed passwords
- Profile management with height, weight, and macro goals
- Food database with search and category filtering
- Daily food logging with quantity tracking
- Real-time daily totals vs goals with remaining macros
- AI-generated 7-day meal plans based on your stats and budget
- Auto-generated API docs at /apidocs

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /signup | Create account |
| POST | /login | Log in, get token |
| PUT | /profile | Set height, weight, and macro goals |
| GET | /foods | List all foods (filter by category) |
| GET | /foods/search?q=chicken | Search foods by name |
| POST | /foods | Add a food to the database |
| POST | /logs | Log a food you ate |
| GET | /logs/today | View daily intake with totals vs goals |
| DELETE | /logs/:id | Remove a log entry |
| POST | /plans | Generate AI meal plan with budget |
| GET | /plans | View past meal plans |

## Run Locally

```bash
git clone https://github.com/AmanShrestha-01/NutriPlan-AI.git
cd NutriPlan-AI
pip install -r requirements.txt
python app.py
```

Visit API docs: http://127.0.0.1:8000/apidocs

## Run Tests

```bash
python test_app.py
```
