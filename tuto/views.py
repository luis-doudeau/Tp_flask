from .app import app, db
from flask import render_template, redirect, url_for, request
from .models import get_sample, get_book_id, get_author, get_info_all_books, delete_livre

from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired


class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators= [DataRequired()])

@app.route("/")
def home():
    return render_template(
        "booksBS.html", 
        title="My Books !",
        books=get_sample())

@app.route("/api/dataBooks", methods = ["POST"])
def dataBooks():
    data = {"data":[]}

    id = request.form["id"]

    titre = request.form["titre"] 

    prix = request.form["prix"] 

    auteur = request.form["auteur"]
    books = get_info_all_books(id, titre, prix, auteur).all()
    for livre in books:
        
        data["data"].append({
            "id" :livre.id,
            "img" : livre.img,
            "titre" : livre.title,
            "prix" :livre.price,
            "auteur" : livre.author.name
        })
    return data

@app.route('/Livres')
def Livres():
    return render_template("gerer_books.html", title= "Livres")

@app.route('/deleteLivre')
def deleteLivre():
    save = delete_livre(request.form["id"])
    return "true" if save == True else save



@app.route("/detail/<id>")
def detail(id):
    book = get_book_id(int(id))
    return render_template(
        "detail.html",
        book=book)

@app.route("/edit/author/<int:id>") 
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name = a.name)
    return render_template("edit_author.html", author=a, form = f)

@app.route ("/save/author/", methods =("POST" ,))
def save_author():
    a = None
    f = AuthorForm ()
    if f. validate_on_submit ():
        id = int(f.id.data)
        a = get_author (id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('one_author', id=a.id ))
    a = get_author (int(f.id.data ))
    return render_template ("edit - author .html", author =a, form=f)