from flask import Blueprint, jsonify, request
from models import db, FoodLog, FoodItem, User
from middleware import get_logged_in_user
import datetime

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["POST"])
def log_food():
    user = get_logged_in_user()

    if not user:
        return jsonify({"error": "You must be logged in"}), 401

    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "food_id" not in data:
        return jsonify({"error": "food_id is required"}), 400

    food = FoodItem.query.get(data["food_id"])

    if not food:
        return jsonify({"error": "Food not found"}), 404

    log = FoodLog(
        user_id=user["user_id"],
        food_id=data["food_id"],
        quantity=data.get("quantity", 1),
        date=datetime.datetime.utcnow().strftime("%Y-%m-%d")
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "Food logged",
        "food": food.name,
        "quantity": log.quantity,
        "calories": food.calories * log.quantity
    }), 201


@logs_bp.route("/logs/today", methods=["GET"])
def get_today():
    user = get_logged_in_user()

    if not user:
        return jsonify({"error": "You must be logged in"}), 401

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    logs = FoodLog.query.filter_by(
        user_id=user["user_id"],
        date=today
    ).all()

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    entries = []

    for log in logs:
        food = FoodItem.query.get(log.food_id)

        cal = food.calories * log.quantity
        pro = food.protein * log.quantity
        carb = food.carbs * log.quantity
        fat_val = food.fat * log.quantity

        total_calories += cal
        total_protein += pro
        total_carbs += carb
        total_fat += fat_val

        entries.append({
            "id": log.id,
            "food_name": food.name,
            "quantity": log.quantity,
            "calories": cal,
            "protein": pro,
            "carbs": carb,
            "fat": fat_val
        })

    db_user = User.query.get(user["user_id"])

    return jsonify({
        "date": today,
        "entries": entries,
        "totals": {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat
        },
        "goals": {
            "calories": db_user.calorie_goal,
            "protein": db_user.protein_goal,
            "carbs": db_user.carb_goal,
            "fat": db_user.fat_goal
        },
        "remaining": {
            "calories": (db_user.calorie_goal or 0) - total_calories,
            "protein": (db_user.protein_goal or 0) - total_protein,
            "carbs": (db_user.carb_goal or 0) - total_carbs,
            "fat": (db_user.fat_goal or 0) - total_fat
        }
    })


@logs_bp.route("/logs/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    user = get_logged_in_user()

    if not user:
        return jsonify({"error": "You must be logged in"}), 401

    log = FoodLog.query.get(log_id)

    if not log:
        return jsonify({"error": "Log not found"}), 404

    if log.user_id != user["user_id"]:
        return jsonify({"error": "This is not your log"}), 403

    db.session.delete(log)
    db.session.commit()

    return jsonify({"message": "Log entry removed"})
