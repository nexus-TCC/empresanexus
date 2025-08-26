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


if __name__ == '__main__':
    app.run(debug=True, port=5001)