from crypt import methods
from .app import app, db
from flask import render_template, redirect, url_for, request
from .models import get_sample, get_book_id, get_author, get_info_all_books, delete_livre, ajouter_livre,\
get_all_info_auteurs, get_nb_livres_auteur, delete_auteur, ajouter_auteur

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

@app.route("/api/dataAuteurs", methods = ["POST"])
def dataAuteurs():
    data = {"data":[]}
    id = request.form["id"]

    nom = request.form["nom"] 


    auteurs = get_all_info_auteurs(id, nom).all()
    for auteur in auteurs:
        data["data"].append({
            "id" :auteur.id,
            "nom" : auteur.name,
            "nbLivres" : get_nb_livres_auteur(auteur.id),
        })
    return data

@app.route('/AddAuteur',methods=['POST'])
def AddAuteur():
    nomAuteur = request.form["NomAuteur"]

    save = ajouter_auteur(nomAuteur)
    return "true" if save == True else save

@app.route('/Auteurs')
def Auteurs():
    return render_template("gerer_author.html", title= "Auteurs")

@app.route('/deleteAuteur', methods = ["POST"])
def deleteAuteur():
    save = delete_auteur(request.form["id"])
    return "true" if save == True else save


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

@app.route('/AddLivre',methods=['POST'])
def AddLivre():
    print("a")
    TitreLivre = request.form["TitreLivre"]
    PrixLivre = int(request.form["PrixLivre"])
    UrlLivre = request.form["UrlLivre"]
    ImageLivre = request.form["ImageLivre"]
    IdAuteurLivre = int(request.form["IdAuteurLivre"])

    save = ajouter_livre(TitreLivre, PrixLivre, UrlLivre, ImageLivre, IdAuteurLivre)
    return "true" if save == True else save

@app.route('/deleteLivre', methods = ["POST"])
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