from .app import db
from sqlalchemy.sql.expression import func


class Author(db.Model):
    """
    Classe Auteur
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    livres = db.relationship('Book', backref='livres', lazy='dynamic')

    def __repr__(self):
        return "%s" % (self.name)


class Book(db.Model):
    """
    Classe Book en lien FK avec Author
    """
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(120))
    url = db.Column(db.String(250))
    img = db.Column(db.String(90))
    author_id = db.Column(db.Integer,
                          db.ForeignKey("author.id"))
    # Champ books qui sera automatiquement renseigné
    # dans la classe Author
    author = db.relationship("Author",
                backref=db.backref("books", lazy="dynamic"))

    def __init__(self,price,title,url,img,author_id):
        self.price = price
        self.title = title
        self.url = url
        self.img = img
        self.author_id = author_id
                
    def __repr__(self):
      return "%s" % (self.title)


def get_sample():
    return Book.query.limit(10).all()

def get_book_id(id):
    return Book.query.get(id)

def get_all_books():
    return Book.query

def get_author(id):
    return Author.query.get(id)

def get_info_all_books(id, titre, prix, auteur):
    res = Book.query
    if(id != ""):
        res = res.filter(Book.id == id)
    if(titre != ""):
        res = res.filter(Book.title == titre)

    if(prix != ""):
        res = res.filter(Book.price == prix)

    if(auteur != ""):
        res = res.filter(Book.author.has(Author.name  == auteur))
    
    return res

def delete_livre(id):
    livre = Book.query.get(id)
    db.session.delete(livre)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
    
def delete_auteur_livre(id):
    livres = Book.query.filter(Book.author.has(Author.id  == id))
    db.session.delete(livres)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
    
def delete_auteur(id):
    delete_auteur_livre(id)
    auteur = Author.query.get(id)
    db.session.delete(auteur)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def ajouter_auteur(nomAuteur):
    auteur = Author(name   = nomAuteur) 
    db.session.add(auteur)

    try:
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
def ajouter_livre(TitreLivre, PrixLivre, UrlLivre, ImageLivre, IdAuteurLivre):
    livre = Book(price   = PrixLivre,
                title   = TitreLivre,
                url     = UrlLivre,
                img     = ImageLivre,
                author_id = IdAuteurLivre) 
    db.session.add(livre)

    try:
        db.session.commit()
        return True
    except Exception as e:
        
        db.session.rollback()
        return repr(e)
    
def get_all_info_auteurs(id, nom):
    res = Author.query
    if(id != ""):
        res = res.filter(Author.id == id)
    if(nom != ""):
        res = res.filter(Author.name == nom)
    return res
    
def get_nb_livres_auteur(id):
    return len(Book.query.filter(Book.author_id == id).all())

def updateAuteur(id, nom):
    auteur = get_author(id)
    auteur.name = nom
    try : 
        db.session.commit()
        return True
    except :
        return False

def get_auteur_by_name(name):
    return Author.query.filter(Author.name == name).first()

def updateLivre(id, titre, prix, url, img, author):
    
    livre = get_book_id(id)
    
    livre.title = titre
    livre.price = prix
    livre.url = url
    livre.img = img
    livre.author = get_auteur_by_name(author)
    
    try : 
        db.session.commit()
        return True
    except :
        db.session.rollback()
        return False