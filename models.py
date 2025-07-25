#models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    livreFavoris = db.Column(db.Text)
    commandes = db.Column(db.Text)

    def __repr__(self):
        return f"User('{self.nom}', '{self.prenom}', '{self.email}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    couverture = db.Column(db.String(120), nullable=False)
    prix = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Book('{self.titre}', '{self.auteur}', '{self.prix}')"