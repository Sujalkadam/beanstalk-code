from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
application = app  # REQUIRED FOR AWS ELASTIC BEANSTALK

# -----------------------------
# DATABASE CONFIG (AWS RDS)
# -----------------------------
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -----------------------------
# DATABASE MODEL
# -----------------------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.name}>"


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    try:
        products = Product.query.all()
        return render_template("index.html", products=products)
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"]
    category = request.form["category"]
    stock = request.form["stock"]

    new_product = Product(
        name=name,
        category=category,
        stock=int(stock),
        status="In Stock" if int(stock) > 0 else "Out of Stock",
        updated_at=datetime.utcnow(),
    )
