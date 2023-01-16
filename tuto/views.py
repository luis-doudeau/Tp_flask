from .app import app
from flask import render_template
from .models import get_sample, get_book_id, get_author

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

class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators= [DataRequired()])

@app.route("/edit/author/<int:id>") 
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name = a.name)
    return render_template("edit_author.html", author=a, form = f)