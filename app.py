from flask import Flask, jsonify
from models import db
from auth.routes import auth_bp, bcrypt
from foods.routes import foods_bp
from logs.routes import logs_bp
from plans.routes import plans_bp
from flasgger import Swagger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"
app.config["SWAGGER"] = {
    "title": "NutriPlan AI",
    "description": "AI-powered nutrition tracking and meal planning API",
    "version": "1.0.0"
}

db.init_app(app)
bcrypt.init_app(app)

swagger = Swagger(app)

app.register_blueprint(auth_bp)
app.register_blueprint(foods_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(plans_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "NutriPlan AI is running"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
