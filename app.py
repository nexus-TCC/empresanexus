from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/' , methods=['GET', 'POST'])
def entrar():
    return render_template('Entrar.html')
@app.route('/continuarGoogle', methods=['GET', 'POST'])
def continuarGoogle():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')
        # Here you would typically handle the login logic, e.g., checking credentials
        return render_template('continuarGoogle.html', email=email)
    return render_template('Index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')
        # Here you would typically handle the registration logic, e.g., saving to a database
        return render_template('cadastro.html', email=email)
    return render_template('Cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
