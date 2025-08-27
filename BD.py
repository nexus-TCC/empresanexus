from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
import bcrypt 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    experiencia = db.Column(db.Text)  # descrição do currículo
    habilidades = db.Column(db.Text)  # lista de skills
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if not usuario:
        return jsonify({"error": "E-mail não cadastrado"}), 400
    if not bcrypt.checkpw(data['senha'].encode('utf-8'), usuario.senha.encode('utf-8')):
        return jsonify({"error": "Senha Incorreta"}), 400
    return jsonify({"message": "Login realizado com sucesso!"})

@app.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"error": "E-mail já cadastrado"}), 400
    senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(
        nome=data['nome', ''],
        email=data['email'],
        senha=senha_hash.decode('utf-8')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"})

@app.route('/criar_banco')
def criar_banco():
    db.create_all()
    return "Banco de dados e tabelas criados!"

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    data = request.get_json()
    senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=senha_hash.decode('utf-8')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário adicionado com sucesso!"})



@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = []
    for usuario in usuarios:
        resultado.append({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email
        })
    return jsonify(resultado)

@app.route('/criar_curriculo', methods=['GET', 'POST'])
def criar_curriculo():
    if request.method == 'POST':
        data = request.form
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
        return jsonify({"message": "Currículo criado com sucesso!"})
    return render_template('CriarCurriculo.html')


@app.route('/criar_empresa', methods=['GET', 'POST'])
def criar_empresa():
    if request.method == 'POST':
        data = request.form
        nova_empresa = Empresa(
            usuario_id=data.get('usuario_id'),
            nome_empresa=data.get('nome_empresa'),
            descricao=data.get('descricao'),
            site=data.get('site'),
            cnpj=data.get('cnpj')
        )
        db.session.add(nova_empresa)
        db.session.commit()
        return jsonify({"message": "Perfil da empresa criado com sucesso!"})
    return render_template('CriarEmpresa.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)