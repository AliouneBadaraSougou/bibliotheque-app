from sqlalchemy import create_engine, MetaData, Table, select
from app import db, Book, app
from sqlalchemy import create_engine, MetaData, Table, select, text


sqlite_engine = create_engine('sqlite:///instance/site.db')
sqlite_metadata = MetaData()
sqlite_metadata.reflect(bind=sqlite_engine)
book_table = Table('book', sqlite_metadata, autoload_with=sqlite_engine)

with app.app_context():
    # Vider la table book sur Neon (attention, supprime tout !)
    db.session.execute(text('DELETE FROM book;'))
    db.session.commit()

    conn = sqlite_engine.connect()
    result = conn.execute(select(book_table))
    books = result.fetchall()

    count = 0
    for row in books:
        prix_str = str(row.prix).replace(',', '.')
        try:
            prix_float = float(prix_str)
        except ValueError:
            prix_float = 0.0

        new_book = Book(
            id=row.id,  # force l'id d'origine
            titre=row.titre,
            auteur=row.auteur,
            description=row.description,
            couverture=row.couverture,
            prix=prix_float
        )
        db.session.add(new_book)
        count += 1
    db.session.commit()
    print(f"{count} livres migrés avec succès et id conservés !")