from .app import db

class Author(db.Model):
    """
    Classe Auteur
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)


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
                
    def __repr__(self):
      return "<Book (%d) %s>" % (self.id, self.title)


def get_sample():
    return Book.query.limit(10).all()

def get_book_id(id):
    return Book.query.get(id)

def get_author(id):
    return Author.query.get(id)

