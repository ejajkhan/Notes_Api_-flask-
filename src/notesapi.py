
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
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

  def __init__(self, name, body):
    self.name = name
    self.body = body


# Note Schema
class NoteSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'body')


# Init schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

db.create_all()


# Create a Note
@app.route('/note', methods=['POST'])
def add_note():
  name = request.json['name']
  body = request.json['body']

  new_note = Note(name, body)

  db.session.add(new_note)
  db.session.commit()

  return note_schema.jsonify(new_note)


# Get All notes
@app.route('/note', methods=['GET'])
def get_notes():
  all_notes = Note.query.all()
  result = notes_schema.dump(all_notes)
  return jsonify(result)


# Get Single notes
@app.route('/note/<id>', methods=['GET'])
def get_note(id):
  note = Note.query.get(id)
  return note_schema.jsonify(note)


# Update a Note
@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
  note = Note.query.get(id)

  name = request.json['name']
  body = request.json['body']

  note.name = name
  note.body = body


  db.session.commit()

  return note_schema.jsonify(note)


# Delete note
@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
  note = Note.query.get(id)
  db.session.delete(note)
  db.session.commit()

  return note_schema.jsonify(note)

# Run Server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
