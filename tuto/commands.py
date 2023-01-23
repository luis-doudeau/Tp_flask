import yaml, os.path
import click
from .app import app, db
from .models import Author, Book


app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username , password):
    "Add a new user."
    from.models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username = username, password = m.hexdigest())
    db.session.add(u)
    db.session.commit()

@app.cli.command()
def syncdb():
    '''
     Création de toutes les tables de la BD
     à partir des models.
    '''
    db.create_all()

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''
     Create all tables and populate them with data in filename
    '''
    db.create_all()

    books = yaml.load(open(filename), Loader=yaml.FullLoader)

    # premier passage : lecture et création des auteurs
    authors = dict()
    for b in books:
        a = b["author"] # nom auteur
        if a not in authors:
            nouveau = Author(name=a)
            # On ajoute l'objet o à la session :
            db.session.add(nouveau)
            authors[a] = nouveau
    # On dit à la DB d'intégrer toutes les nouvelles données
    # des id vont être automatiquement créés pour les auteurs
    db.session.commit()

    # Création des livres
    for b in books:
        # on récupère l'auteur par son nom
        a = authors[b["author"]]
        # on instancie le livre
        book = Book(price   = b["price"],
                    title   = b["title"],
                    url     = b["url"],
                    img     = b["img"],
                    author_id = a.id) 
    # On ajoute l'objet book à la Base :
        db.session.add(book)
    db.session.commit()



