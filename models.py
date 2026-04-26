from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    calorie_goal = db.Column(db.Float, nullable=True)
    protein_goal = db.Column(db.Float, nullable=True)
    carb_goal = db.Column(db.Float, nullable=True)
    fat_goal = db.Column(db.Float, nullable=True)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    food_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1)
    date = db.Column(db.String, nullable=False)

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String, nullable=False)
