from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# parte pro daniel mecher (dnd)
# Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Postagem
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reposts = db.Column(db.Integer, default=0)
    reply_to = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    user = db.relationship('User', backref='posts')

# Sala (Room)
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship('User', backref='rooms')
