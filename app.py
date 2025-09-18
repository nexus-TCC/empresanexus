from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura' # Necessária para usar a sessão

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'
    
class Profissional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(50))
    endereco = db.Column(db.String(200))
    experiencia = db.Column(db.Text) 
    habilidades = db.Column(db.Text) 
    usuario = db.relationship('Usuario', backref='profissional', uselist=False)

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    nome_empresa = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    site = db.Column(db.String(200))
    cnpj = db.Column(db.String(50), unique=True)
    usuario = db.relationship('Usuario', backref='empresa', uselist=False)

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text)
    local = db.Column(db.String(150))
    empresa = db.relationship('Empresa', backref='vagas')

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/entrar' , methods=['GET', 'POST'])
def mostrar_login():
    return render_template('Entrar.html')
    
@app.route('/criarConta' , methods=['GET', 'POST'])
def mostrar_cadastro():
    return render_template('CriarConta.html')

@app.route('/index')
def index():
    return render_template('Index.html')

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    email =  data.get('email')
    senha = data.get('senha')
    nome = data.get('nome', '')
    if not all ([email, senha, nome]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já cadastrado"}), 409
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(nome=nome, email=email, senha=hashed_senha.decode('utf-8'))
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    if not all ([email, senha]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "E-mail ou senha incorretos"}), 401
    if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        session['usuario_id'] = usuario.id
        return jsonify({"message": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"error": "E-mail ou senha incorretos"}), 401
    
@app.route('/api/criar_curriculo', methods=['POST'])
def criar_curriculo():
    data = request.get_json()
    novo_curriculo = Profissional(
        usuario_id=data.get('usuario_id'),
        nome=data.get('nome'),
        telefone=data.get('telefone'),
        endereco=data.get('endereco'),
        experiencia=data.get('experiencia'),
        habilidades=data.get('habilidades')
    )
    db.session.add(novo_curriculo)
    db.session.commit()
    return jsonify({"message": "Currículo criado com sucesso!"}), 201

@app.route('/api/criar_empresa', methods=['POST'])
def criar_empresa():
    data = request.get_json()
    nova_empresa = Empresa(
        usuario_id=data.get('usuario_id'),
        nome_empresa=data.get('nome_empresa'),
        descricao=data.get('descricao'),
        site=data.get('site'),
        cnpj=data.get('cnpj')
    )
    db.session.add(nova_empresa)
    db.session.commit()
    return jsonify({"message": "Perfil criado com sucesso!"}), 201

@app.route('/criar_banco')
def criar_banco():
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
