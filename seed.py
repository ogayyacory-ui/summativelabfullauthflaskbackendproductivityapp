from app import create_app
from extensions import db
from models import User, Note

app = create_app()

with app.app_context():
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    print("Seeding users...")
    user1 = User(username="alice", email="alice@example.com")
    user1.set_password("password123")

    user2 = User(username="bob", email="bob@example.com")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding notes...")
    # Alice's notes
    for i in range(1, 15):
        db.session.add(Note(
            title=f"Alice's Note #{i}",
            content=f"Content for Alice's note {i}.",
            user_id=user1.id
        ))

    # Bob's note
    db.session.add(Note(
        title="Bob's Secret Note",
        content="This is private to Bob.",
        user_id=user2.id
    ))

    db.session.commit()
    print("Seeding complete! Log in as alice@example.com or bob@example.com.")