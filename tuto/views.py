from .app import app
from flask import render_template
from .models import get_sample, get_book_id

from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired


@app.route("/")
def home():
    return render_template(
        "booksBS.html", 
        title="My Books !",
        books=get_sample())


@app.route("/detail/<id>")
def detail(id):
    book = get_book_id(int(id))
    return render_template(
        "detail.html",
        book=book)