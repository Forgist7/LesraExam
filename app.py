from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@db:5432/{os.getenv('POSTGRES_DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    score = data.get('score')
    if name and score is not None:
        record = Record(name=name, score=score)
        db.session.add(record)
        db.session.commit()
        return jsonify({"message": "Record added successfully"}), 201
    return jsonify({"error": "Invalid data"}), 400


@app.route('/results', methods=['GET'])
def results():
    records = Record.query.all()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "score": r.score,
        "timestamp": r.timestamp.isoformat()
    } for r in records])


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
###