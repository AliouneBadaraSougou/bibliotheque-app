#config.py

from app import app, db, bcrypt
from models import User

def create_admin():
    with app.app_context():
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            print('L\'administrateur existe déjà.')
            return
        
        hashed_password = bcrypt.generate_password_hash('senegalaise').decode('utf-8')
        
        admin = User(nom='Admin', prenom='Admin', email='ibrahimasougou@gmail.com', password=hashed_password, is_admin=True)
        
        db.session.add(admin)
        db.session.commit()
        
        print('Admin ajouté avec succès.')
        print(f"Admin email: {admin.email}")
        print(f"Admin hashed_password: {admin.password}")

if __name__ == '__main__':
    create_admin()
