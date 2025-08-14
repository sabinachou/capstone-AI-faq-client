from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import uuid

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define FAQ model
class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

with app.app_context():
    print("🔍 Testing connection to Azure PostgreSQL...")

    # 1️⃣ Create
    new_question = f"Test question {uuid.uuid4()}"
    new_answer = "This is a test answer."
    faq = FAQ(question=new_question, answer=new_answer)
    db.session.add(faq)
    db.session.commit()
    print(f"✅ Inserted: {faq.id} - {faq.question}")

    # 2️⃣ Read
    fetched = FAQ.query.filter_by(id=faq.id).first()
    print(f"🔍 Fetched: {fetched.id} - {fetched.question} -> {fetched.answer}")

    # 3️⃣ Update
    fetched.answer = "Updated test answer."
    db.session.commit()
    print(f"✏️ Updated: {fetched.id} - {fetched.answer}")

    # 4️⃣ Delete
    db.session.delete(fetched)
    db.session.commit()
    print(f"🗑 Deleted: {faq.id}")

    print("🎉 CRUD test completed successfully.")