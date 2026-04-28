from flask import Blueprint, jsonify, request
from models import db, FoodItem

foods_bp = Blueprint("foods", __name__)


@foods_bp.route("/foods", methods=["GET"])
def get_foods():
    category = request.args.get("category", "")

    if category:
        foods = FoodItem.query.filter_by(category=category).all()
    else:
        foods = FoodItem.query.all()

    result = []

    for f in foods:
        result.append({
            "id": f.id,
            "name": f.name,
            "calories": f.calories,
            "protein": f.protein,
            "carbs": f.carbs,
            "fat": f.fat,
            "serving_size": f.serving_size,
            "category": f.category
        })

    return jsonify(result)


@foods_bp.route("/foods/search", methods=["GET"])
def search_foods():
    query = request.args.get("q", "")

    if len(query) == 0:
        return jsonify({"error": "Provide a search term with ?q=something"}), 400

    results = FoodItem.query.filter(FoodItem.name.contains(query)).all()

    result = []

    for f in results:
        result.append({
            "id": f.id,
            "name": f.name,
            "calories": f.calories,
            "protein": f.protein,
            "carbs": f.carbs,
            "fat": f.fat,
            "serving_size": f.serving_size,
            "category": f.category
        })

    return jsonify(result)


@foods_bp.route("/foods", methods=["POST"])
def add_food():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = [
        "name",
        "calories",
        "protein",
        "carbs",
        "fat",
        "serving_size",
        "category"
    ]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    food = FoodItem(
        name=data["name"],
        calories=data["calories"],
        protein=data["protein"],
        carbs=data["carbs"],
        fat=data["fat"],
        serving_size=data["serving_size"],
        category=data["category"]
    )

    db.session.add(food)
    db.session.commit()

    return jsonify({
        "id": food.id,
        "name": food.name,
        "message": "Food added"
    }), 201
