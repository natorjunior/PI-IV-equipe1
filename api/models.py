from database import db
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin

# Fuso horário de Fortaleza (UTC-3)
FORTALEZA_TZ = timezone(timedelta(hours=-3))

# Tabela de associação
tabela_curtidas = db.Table('curtidas_assoc',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('postagem_id', db.Integer, db.ForeignKey('postagens.id'), primary_key=True)
)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    postagens = db.relationship('Postagem', backref='autor', lazy=True)

    # Métodos necessários para Flask-Login (já fornecidos por UserMixin)
    # is_authenticated, is_active, is_anonymous, get_id()
    
    def __repr__(self):
        return f"<Usuario {self.nome_usuario}>"

class Postagem(db.Model):
    __tablename__ = 'postagens'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    imagem_url = db.Column(db.String(500), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(FORTALEZA_TZ))
    
    curtidas = db.Column(db.Integer, default=0)

    quem_curtiu = db.relationship('Usuario', secondary=tabela_curtidas, lazy='subquery',
        backref=db.backref('posts_curtidos', lazy=True))

    @property
    def total_curtidas(self):
        return self.curtidas
    
    def __repr__(self):
        return f"<Postagem {self.id}>"

class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    user = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(FORTALEZA_TZ))

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user': self.user,
            'text': self.text,
            'time': self.timestamp.strftime('%H:%M')
        }

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'public' ou 'private'
    password = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(FORTALEZA_TZ))
    mensagens = db.relationship('Mensagem', backref='sala', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'objective': self.objective,
            'type': self.type,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M')
        }
    
    def __repr__(self):
        return f"<Sala {self.name}>"