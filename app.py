#app.py
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
# Importer les modèles après l'initialisation des extensions pour éviter les erreurs circulaires
from models import db, User, Book

# Initialiser l'application
app = Flask(__name__)
app.config.from_object(Config)

# Initialiser les extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'
login_manager.login_message_category = 'info'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/search', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query', '')
    if query:
        # Rechercher dans le titre, l'auteur et la description des livres
        results = Book.query.filter(
            (Book.titre.ilike(f'%{query}%')) |
            (Book.auteur.ilike(f'%{query}%')) |
            (Book.description.ilike(f'%{query}%'))
        ).all()
    else:
        results = []
    
    return render_template('menu.html', books=results) 

@app.route('/commander/<int:book_id>', methods=['GET', 'POST'])
@login_required
def commander(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash('Livre non trouvé.', 'danger')
        return redirect(url_for('menu_route'))

    if request.method == 'POST':
        localisation = request.form.get('localisation')
        telephone = request.form.get('telephone')
        if localisation and telephone:
            # Enregistrer la commande et supprimer le livre du menu
            current_user.commandes = (current_user.commandes or '') + f"{book_id},"
            db.session.delete(book)
            db.session.commit()
            flash('Commande passée avec succès.', 'success')
            return redirect(url_for('confirmation_commande', book_id=book_id, localisation=localisation, telephone=telephone))
    elif request.method == 'GET' and request.args.get('confirm'):
        return render_template('commander.html', book=book)

    return render_template('commander.html', book=book)



@app.route('/confirmation_commande/<int:book_id>')
@login_required
def confirmation_commande(book_id):
    localisation = request.args.get('localisation')
    telephone = request.args.get('telephone')
    
    book = Book.query.get(book_id)
    if not book:
        flash('Livre non trouvé.', 'danger')
        return redirect(url_for('menu_route'))

    return render_template('confirmer_commande.html', book=book, localisation=localisation, telephone=telephone)



# Route pour gérer le profil de l'utilisateur
@app.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    if request.method == 'POST':
        # Logique pour mettre à jour le profil de l'utilisateur (à implémenter)
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('manage_profile'))
    return render_template('manage_profile.html', Book=Book)

# Route pour ajouter un livre aux favoris
@app.route('/add_to_favorites/<int:book_id>', methods=['POST'])
@login_required
def add_to_favorites(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash('Livre non trouvé.', 'danger')
        return redirect(url_for('menu_route'))

    if current_user.is_authenticated:
        if current_user.livreFavoris:
            current_user.livreFavoris += f"{book_id},"
        else:
            current_user.livreFavoris = f"{book_id},"
        
        db.session.commit()
        flash('Livre ajouté aux favoris avec succès.', 'success')
        return redirect(url_for('menu_route'))
    else:
        flash('Vous devez être connecté pour ajouter des favoris.', 'danger')
        return redirect(url_for('connexion'))

# Route pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('index'))

# Route pour le menu utilisateur
@app.route('/menu')
@login_required
def menu_route():
    books = Book.query.all()
    for book in books:
        print(f"Titre: {book.titre}, Prix: {book.prix}")
    return render_template('menu.html', books=books)


# Route pour le tableau de bord administrateur
@app.route('/admin_dashboard')
@login_required
def admin_dashboard_route():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))

    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_dashboard.html', users=users, books=books)

# Route pour l'accueil
@app.route('/')
def index():
    books = Book.query.limit(6).all()
    return render_template('index.html', books=books)

# Route pour l'API des livres en vedette
@app.route('/api/featured_books')
def api_featured_books():
    books = Book.query.limit(6).all()
    return jsonify([{
        'id': book.id,
        'title': book.titre,
        'author': book.auteur,
        'description': book.description,
        'imageUrl': url_for('static', filename='images/' + book.couverture)
    } for book in books])

# Route pour l'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(nom=nom, prenom=prenom, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('connexion'))
    return render_template('inscription.html')

# Route pour la connexion utilisateur
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Connexion réussie', 'success')
            return redirect(url_for('menu_route'))
        else:
            flash('Échec de la connexion. Veuillez vérifier votre email et mot de passe', 'danger')
    return render_template('connexion.html')

# Route pour la connexion administrateur
@app.route('/connexion_admin', methods=['GET', 'POST'])
def connexion_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Connexion réussie', 'success')
            return redirect(url_for('admin_dashboard_route'))
        else:
            flash('Logins invalide. Vous n\'êtes pas administrateur.', 'danger')
    return render_template('connexion_admin.html')

# Route pour ajouter un administrateur
@app.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(nom='Admin', prenom='Admin', email=email, password=hashed_password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        flash('Nouvel administrateur ajouté avec succès.', 'success')
        return redirect(url_for('admin_dashboard_route'))

    return render_template('add_admin.html')

# Route pour ajouter un utilisateur (admin)
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(nom=nom, prenom=prenom, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Nouvel utilisateur ajouté avec succès.', 'success')
        return redirect(url_for('admin_dashboard_route'))

    return render_template('add_user.html')

# Route pour supprimer un utilisateur
@app.route('/remove_user/<int:user_id>', methods=['POST'])
@login_required
def remove_user(user_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé avec succès.', 'success')
    else:
        flash('Utilisateur introuvable.', 'danger')
    return redirect(url_for('admin_dashboard_route'))

# Route pour supprimer un livre
@app.route('/remove_book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(book_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Livre supprimé avec succès.', 'success')
    else:
        flash('Livre introuvable.', 'danger')
    return redirect(url_for('admin_dashboard_route'))

# Route pour supprimer un administrateur
@app.route('/remove_admin/<int:admin_id>', methods=['POST'])
@login_required
def remove_admin(admin_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    admin = User.query.get(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        flash('Administrateur supprimé avec succès.', 'success')
    else:
        flash('Administrateur introuvable.', 'danger')
    return redirect(url_for('admin_dashboard_route'))

# Exécuter l'application
if __name__ == '__main__':
    app.run(debug=True)
