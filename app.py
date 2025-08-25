from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Here you would typically handle the login logic, e.g., checking credentials
        return render_template('Entrar.html', email=email, senha=senha)
    return render_template('Entrar.html')
    
@app.route('/continuar-google', methods=['GET', 'POST'])
def continuarGoogle():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Here you would typically handle the login logic, e.g., checking credentials
        return render_template('ContinuarGoogle.html', email=email, senha=senha)
    return render_template('ContinuarGoogle.html')



if __name__ == '__main__':
    app.run(debug=True)
