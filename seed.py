from app import create_app
from extensions import db
from models import User, Note

app = create_app()

with app.app_context():
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    print("Seeding users...")
    kamau = User(username="Kamau", email="kamau@example.com")
    kamau.set_password("87mau")

    kiprotich = User(username="kiprotich", email="kiprotich@example.com")
    kiprotich.set_password("kip2027")

    db.session.add_all([kamau, kiprotich])
    db.session.commit()

    print("Seeding notes...")
    # kamau's notes
    for i in range(1, 15):
        db.session.add(Note(
            title=f"Alice's Note #{i}",
            content=f"Content for Alice's note {i}.",
            user_id=kamau.id
        ))

    # Bob's note
    db.session.add(Note(
        title="Bob's Secret Note",
        content="This is private to Bob.",
        user_id=kiprotich.id
    ))

    db.session.commit()
    print("Seeding complete! Log in as alice@example.com or bob@example.com.")