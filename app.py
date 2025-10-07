from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt 
import os


app = Flask(__name__)

# Configurações do Aplicativo
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_dev_insegura')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///users.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelos SQLAlchemy ---
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo_conta = db.Column(db.String(20), nullable=False) 
    
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

# --- Rotas de Navegação (Views) ---

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/entrar' , methods=['GET', 'POST'])
def mostrar_login():
    return render_template('Entrar.html')

@app.route('/tipoConta' , methods=['GET', 'POST'])
def mostrar_tipo_conta():
    return render_template('TipoConta.html')
    
# Rota para o formulário de Cadastro de Profissional
@app.route('/criarContaProfissional' , methods=['GET', 'POST'])
def mostrar_cadastro_profissional():
    # Passa o tipo de conta para o HTML
    return render_template('CriarContaProfissional.html', tipo_conta='profissional')

# Rota para o formulário de Cadastro de Empresa
@app.route('/criarContaEmpresa' , methods=['GET', 'POST'])
def mostrar_cadastro_empresa():
    # Passa o tipo de conta para o HTML
    return render_template('CriarContaEmpresa.html', tipo_conta='empresa')

@app.route('/index')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('Index.html'))

# Rotas API

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    nome = data.get('nome', '')
    tipo_conta = data.get('tipo_conta') 
    
    if not all ([email, senha, nome, tipo_conta]):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    if tipo_conta not in ['profissional', 'empresa']:
        return jsonify({"error": "Tipo de conta inválido"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já cadastrado"}), 409

    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(
        nome=nome, 
        email=email, 
        senha=hashed_senha.decode('utf-8'), 
        tipo_conta=tipo_conta
    )

    db.session.add(novo_usuario)
    db.session.commit()
    
    session['usuario_id'] = novo_usuario.id 
    session['tipo_conta'] = novo_usuario.tipo_conta # Armazena na sessão

    return jsonify({"message": "Usuário cadastrado com sucesso!", "tipo_conta": novo_usuario.tipo_conta}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not all ([email, senha]):
        return jsonify({"success": False, "error": "Todos os campos são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "E-mail ou senha incorretos"}), 401

    if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        session['usuario_id'] = usuario.id
        return jsonify({"success": True, "message": "Login realizado com sucesso!"}), 200
    else:
        return jsonify({"success": False, "error": "E-mail ou senha incorretos"}), 401

@app.route('/api/criar_curriculo', methods=['POST'])
def criar_curriculo():
    usuario_id = session.get('usuario_id')
    tipo_conta = session.get('tipo_conta')

    # Se não está logado, 401 (Não Autorizado/Não Autenticado)
    if not usuario_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
        
    # Se o tipo de conta não é 'profissional' para esta rota, 403 (Proibido)
    if tipo_conta != 'profissional':
        return jsonify({"error": "Acesso negado. Apenas para profissionais."}), 403
    
    if Profissional.query.filter_by(usuario_id=usuario_id).first():
        return jsonify({"error": "Perfil de profissional já existe para este usuário"}), 409
    
    

    data = request.get_json()
    novo_curriculo = Profissional(
        usuario_id=usuario_id,
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

    usuario_id = session.get('usuario_id')
    if not usuario_id or session.get('tipo_conta') != 'empresa':
        return jsonify({"error": "Acesso negado ou usuário não autenticado"}), 403
    if not usuario_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
    
    if Empresa.query.filter_by(usuario_id=usuario_id).first():
        return jsonify({"error": "Perfil de empresa já existe para este usuário"}), 409

    data = request.get_json()
    nova_empresa = Empresa(
        usuario_id=usuario_id,
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
    return "Banco criado"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)