# Ce script lit les users de SQLite et les insère dans Neon
from app import db, User  # adapte selon ton projet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connexion à SQLite
sqlite_engine = create_engine('sqlite:///instance/site.db')
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# Connexion à Neon (déjà configurée dans ton app Flask)
from app import app
with app.app_context():
    users = sqlite_session.query(User).all()
    for user in users:
        # Crée un nouvel utilisateur pour Neon
        new_user = User(
            nom=user.nom,
            prenom=user.prenom,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin,
            livreFavoris=user.livreFavoris,
            commandes=user.commandes
        )
        db.session.add(new_user)
    db.session.commit()