from crypt import methods
from .app import app, db, login_manager
from flask import render_template, redirect, url_for, request
from .models import Author, Book, get_sample, get_book_id, get_author, get_info_all_books, delete_livre, ajouter_livre,\
get_all_info_auteurs, get_nb_livres_auteur, delete_auteur, ajouter_auteur, updateAuteur, updateLivre, User, get_user
from flask_login import login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
import click


@login_manager.user_loader
def load_user(username):
    return get_user(username)


@app.route("/")
def home():
    return render_template("booksBS.html", title="Mes Livres !", books=get_sample())

class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom", validators= [DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField ()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256 ()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None


@app.route ("/login", methods =("GET","POST"))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template ("login.html", form=f)


@app.route ("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/admin")
def admin():
    print(current_user)
    if current_user.isadmin :
        return render_template("admin.html")
    else : 
        return render_template("booksBS.html", title="My Books !", books=get_sample())

@app.route("/api/dataAuteurs", methods = ["POST"])
@login_required
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
@login_required
def AddAuteur():
    nomAuteur = request.form["NomAuteur"]

    save = ajouter_auteur(nomAuteur)
    return "true" if save == True else save

@app.route('/Auteurs')
@login_required
def Auteurs():
    if not current_user.admin:
        return redirect("/")

    return render_template("gerer_author.html", title= "Auteurs")

@app.route('/deleteAuteur', methods = ["POST"])
@login_required
def deleteAuteur():
    auteur = get_author(request.form["id"])
    db.session.delete(auteur)
    try:
        db.session.commit()
        return "true"
    except:
        db.session.rollback()
        return "false"
    
@app.route("/Admin/AuteurDetail/<id>")
@login_required
def AuteurDetail(id):
    if(id == "null"):
        return render_template(
        "detail_auteur.html",auteur=Author(""),livres_auteur ="")
        
    livre = ""
    for l in Author.query.get(id).livres.all():
        livre += l.__repr__() + "|" 
    return render_template(
        "detail_auteur.html",auteur=get_author(id),livres_auteur = livre)

@app.route("/UpdateAuteur",methods =["POST"])
@login_required
def UpdateAuteur():
    name = request.form["name"]
    id = request.form["id"]
    new = request.form["isnew"]
    if(new == "false"):
        save = updateAuteur(id,name)
    else:
        save = ajouter_auteur(name)
    
    return "true" if save else "false"

@app.route("/api/dataBooks", methods = ["POST"])
@login_required
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
                "auteur" : livre.author.__repr__()
        })
    
    return data

@app.route('/Livres')
@login_required
def Livres():
    if not current_user.admin:
        return redirect("/")
    return render_template("gerer_books.html", title= "Livres")

@app.route('/AddLivre',methods=['POST'])
@login_required
def AddLivre():
    TitreLivre = request.form["TitreLivre"]
    PrixLivre = int(request.form["PrixLivre"])
    UrlLivre = request.form["UrlLivre"]
    ImageLivre = request.form["ImageLivre"]
    IdAuteurLivre = int(request.form["IdAuteurLivre"])

    save = ajouter_livre(TitreLivre, PrixLivre, UrlLivre, ImageLivre, IdAuteurLivre)
    return "true" if save == True else save

@app.route("/deleteLivre",methods = ["POST"])
@login_required
def deleteLivre():
    livre = get_book_id(request.form["id"])
    db.session.delete(livre)
    try:
        db.session.commit()
        return "true"
    except:
        db.session.rollback()
        return "false"

@app.route("/UpdateLivre",methods =["POST"])
@login_required
def UpdateLivre():
    
    id = request.form["id"]
    title = request.form["title"]
    price = request.form["price"]
    author = request.form["author"]
    url = request.form["url"]
    img = request.form["img"]
    new = request.form["new"]
        
    if(new == "false"):
        save =  updateLivre(id, title, price, url, img, author)
    else:
        save = ajouter_livre(title, price, url, img, author)
    
    return "true" if save else "false"

@app.route("/Admin/LivreDetail/<id>")
@login_required
def LivreDetail(id):
    if(id == "null"):
        return render_template(
        "detail_livre.html", livre = Book("", "", "", "", Author("")), auteurs = Author.query.all())
    return render_template(
        "detail_livre.html", livre = get_book_id(id),auteurs = Author.query.all())

@app.route("/Client/Livres")
@login_required
def ClientLivres():
    return render_template("livres.html", title= "Livres")

@app.route("/Client/Auteurs")
@login_required
def ClientAuteurs():
    return render_template("auteurs.html", title= "Auteurs")

@app.route("/Admin")
@login_required
def Admin():
    if not current_user.admin:
        return redirect("/")
    return render_template("admin.html", title= "Admin")

@app.route("/detail/<id>")
@login_required
def detail(id):
    book = get_book_id(int(id))
    return render_template(
        "detail.html",
        book=book)

@app.route ("/save/author/", methods =("POST" ,))
@login_required
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