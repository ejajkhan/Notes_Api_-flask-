
from datetime import datetime, time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_kEY'] = 'aronno'
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Note Class/Model
class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  body = db.Column(db.String(200))
  creationTime = db.Column(db.DateTime, default=datetime.utcnow)

  def to_dict(self):
    return dict(
      id=self.id,
      name=self.name,
      body=self.body,
      creationTime= self.creationTime,
    )

db.create_all()


# Create a Note
@app.route('/note', methods=['POST'])
def add_note():
  data=request.get_json()
  note = Note(name=data['name'],body=data['body'])

  db.session.add(note)
  db.session.commit()

  return jsonify(note.to_dict())


# Get All notes
@app.route('/note', methods=['GET'])
def get_notes():
  all_notes = Note.query.all()
  return jsonify([n.to_dict() for n in all_notes])


# Get Single notes
@app.route('/note/<id>', methods=['GET'])
def get_note(id):
  note = Note.query.get(id)
  return jsonify([ note.to_dict() ])


# Update a Note
@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
  note = Note.query.get(id)

  name = request.json['name']
  body = request.json['body']

  note.name = name
  note.body = body
  db.session.commit()
  
  return jsonify([note.to_dict()])


# Delete note
@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
  note = Note.query.get(id)
  db.session.delete(note)
  db.session.commit()

  return jsonify(note.to_dict())

# Run Server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
