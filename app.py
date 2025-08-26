from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/minha-rota', methods=['POST'])
def minha_rota():
    dados = request.get_json()
    # Processa os dados recebidos do JS
    resposta = {'mensagem': 'Dados recebidos!', 'dados': dados}
    return jsonify(resposta)

@app.route('/entrar' , methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Here you would typically handle the login logic, e.g., checking credentials
        return render_template('Entrar.html', email=email, senha=senha)
    return render_template('Entrar.html')
    
@app.route('/CriarConta' , methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Here you would typically handle the account creation logic
        return render_template('CriarConta.html', email=email, senha=senha)
    return render_template('CriarConta.html')

@app.route('/index')
def index():
    return render_template('Index.html')




if __name__ == '__main__':
    app.run(debug=True)
