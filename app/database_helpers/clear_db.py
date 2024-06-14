from app import create_app, db

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Recreate all tables
    print("Database cleared and tables recreated.")
