from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
    
@app.route('/criar_banco')
def criar_banco():
    db.create_all()
    return "Banco de dados e tabelas criados!"

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    data = request.get_json()
    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=dados['senha']
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
        } for usuario in usuarios)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)