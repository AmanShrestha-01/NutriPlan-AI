from flask import Blueprint, jsonify, request
from models import db, MealPlan, User
from middleware import get_logged_in_user
import datetime
import requests as http_requests
import os

plans_bp = Blueprint("plans", __name__)

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")

def call_claude(prompt):
    response = http_requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    return data["content"][0]["text"]

@plans_bp.route("/plans", methods=["POST"])
def generate_plan():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "budget" not in data:
        return jsonify({"error": "budget is required"}), 400
    db_user = User.query.get(user["user_id"])
    if not db_user.calorie_goal:
        return jsonify({"error": "Set your goals first with PUT /profile"}), 400
    prompt = f"""Create a detailed 7-day meal plan for someone with these stats and goals:

Height: {db_user.height}
Weight: {db_user.weight}
Daily calorie goal: {db_user.calorie_goal}
Daily protein goal: {db_user.protein_goal}g
Daily carb goal: {db_user.carb_goal}g
Daily fat goal: {db_user.fat_goal}g
Weekly budget: ${data['budget']}

For each day, provide breakfast, lunch, dinner, and snacks.
Include estimated calories and macros for each meal.
Keep meals simple, affordable, and within the budget.
Include a grocery list at the end with estimated costs."""
    try:
        content = call_claude(prompt)
        plan = MealPlan(
            user_id=user["user_id"],
            content=content,
            budget=data["budget"],
            created_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(plan)
        db.session.commit()
        return jsonify({
            "message": "Meal plan generated",
            "plan_id": plan.id,
            "content": content,
            "budget": plan.budget
        })
    except Exception as e:
        return jsonify({"error": "AI request failed", "details": str(e)}), 500

@plans_bp.route("/plans", methods=["GET"])
def get_plans():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    plans = MealPlan.query.filter_by(user_id=user["user_id"]).all()
    result = []
    for p in plans:
        result.append({
            "id": p.id,
            "budget": p.budget,
            "content": p.content,
            "created_at": p.created_at
        })
    return jsonify(result)
