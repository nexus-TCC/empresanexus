from db import db
from sqlalchemy import func, UniqueConstraint
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo_conta = db.Column(db.String(20), nullable=False) 
    
    def get_id(self):
        return str(self.id)
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
        
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
class Profissional(db.Model):
    __tablename__ = 'profissionais'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    nome_profissional = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(15))
    telefone = db.Column(db.String(50))
    experiencia = db.Column(db.Text) 
    habilidades = db.Column(db.Text) 
    usuario = db.relationship('Usuario', backref=db.backref('profissional', uselist=False))

class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    nome_empresa = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(15))
    descricao = db.Column(db.Text)
    site = db.Column(db.String(200))
    cnpj = db.Column(db.String(50), unique=True)
    usuario = db.relationship('Usuario', backref=db.backref('empresa', uselist=False))
    vagas = db.relationship('Vaga', backref='empresa', lazy='dynamic')

class Vaga(db.Model):
    __tablename__ = 'vagas'
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False) 
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text)
    local = db.Column(db.String(150))
    salario = db.Column(db.Numeric(10,2))

class Candidatura(db.Model):
    __tablename__ = 'candidaturas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave Estrangeira: Referência ao Profissional que se candidatou
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    
    # Chave Estrangeira: Referência à Vaga para a qual se candidatou
    vaga_id = db.Column(db.Integer, db.ForeignKey('vagas.id'), nullable=False)
    
    # Campos Adicionais
    data_candidatura = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Pendente', nullable=False) # Ex: Pendente, Visualizada, Aceita, Rejeitada
    
    # Relacionamentos (opcional, mas recomendado)
    profissional = db.relationship('Profissional', backref='candidaturas')
    vaga = db.relationship('Vaga', backref='candidaturas')
    
    def __repr__(self):
        return f"<Candidatura id={self.id} Status={self.status}>"
