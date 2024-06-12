# run.py
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Ensure that database tables are created

if __name__ == "__main__":
    app.run(debug=True)
