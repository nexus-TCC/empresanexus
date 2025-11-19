from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from db import db
from models import Usuario, Profissional, Empresa, Vaga
from utils import formatar_cards_vagas, formatar_cards_profissionais
import bcrypt
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = 'AcabaPeloAmorDeDeus'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.after_request
def add_security_headers(response):

    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response

def inicializar_dados_ficticios(app):
    with app.app_context():
        if Usuario.query.first():
            print("Dados fictícios já existem. Pulando inicialização.")
            return
        print("Criando dados fictícios mínimos...")

        ADMIN_EMAIL = 'nexus.tcc4@gmail.com'
        ADMIN_SENHA = 'nexustccetec'
        admin_senha_hash = bcrypt.hashpw(ADMIN_SENHA.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        SENHA_PROFISSIONAL = '123456'
        profissional_senha_hash = bcrypt.hashpw(SENHA_PROFISSIONAL.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario_admin = Usuario(nome='Admin Nexus', email=ADMIN_EMAIL, senha=admin_senha_hash, tipo_conta='empresa')
        usuario_profissional = Usuario(nome='Ana Curriculo', email='ana@curriculo.com', senha=profissional_senha_hash, tipo_conta='profissional')

        db.session.add_all([usuario_admin, usuario_profissional])
        db.session.commit()
       
       
        empresa_admin = Empresa(
            usuario_id=usuario_admin.id,
            nome_empresa='Nexus Corp',
            endereco='Av. Principal, 100',
            cidade='São Paulo',
            estado='SP',
            cep='01310-100',
            descricao='Empresa de teste para demonstração do sistema.',
            cnpj='12.345.678/0001-90'
        )
        profissional_ana = Profissional(
            usuario_id=usuario_profissional.id,
            nome_profissional='Ana Curriculo',
            endereco='Rua Fictícia, 1',
            cidade='Rio de Janeiro',
            estado='RJ',
            cep='20000-000',
            telefone='(21) 98765-4321',
            experiencia='5 anos de experiência em Testes de Software e Garantia de Qualidade.',
            habilidades='QA, Testes Automatizados, Selenium, Inglês Fluente'
        )
        db.session.add_all([empresa_admin, profissional_ana])
        db.session.commit()
        # --- 3. Vaga de Exemplo ---
        vaga_1 = Vaga(
            empresa_id=empresa_admin.id,
            titulo='Analista de QA Pleno (Híbrido)',
            descricao='Vaga para garantir a qualidade de nossos produtos digitais, focando em testes de regressão e performance.',
            requisitos='Mínimo 3 anos de experiência em QA. Conhecimento em metodologias ágeis.',
            local='São Paulo / Híbrido'
        )
        db.session.add(vaga_1)
        db.session.commit()
        
        print("Dados fictícios mínimos criados com sucesso!")
        
@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/entrar' , methods=['GET', 'POST'])
def mostrar_login():
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    return render_template('Entrar.html')

@app.route('/tipoConta' , methods=['GET', 'POST'])
def mostrar_tipo_conta():
    return render_template('TipoConta.html')


@app.route('/criarContaProfissional' , methods=['GET', 'POST'])
def mostrar_cadastro_profissional():
    return render_template('CriarContaProfissional.html', tipo_conta='profissional')

@app.route('/criarContaEmpresa' , methods=['GET', 'POST'])
def mostrar_cadastro_empresa():
    return render_template('CriarContaEmpresa.html', tipo_conta='empresa')

@app.route('/curriculo')
def criar_curriculo():
    return render_template('CriarCurriculo.html')

@app.route('/vaga')
def mostrar_vaga():
    # Redireciona para o formulário de criação de vaga, se for uma empresa
    if session.get('tipo_conta') == 'empresa':
        return redirect(url_for('criar_vaga'))
    return redirect(url_for('index'))

@app.route('/api/search_data', methods=['GET'])
def search_data():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401

    termo = request.args.get('termo', '').strip()
    tipo_conta = session.get('tipo_conta')
    cards_filtrados = []

    if not termo:
        # Se o termo estiver vazio, retorna todos os cards (opcionalmente pode retornar vazio)
        return redirect(url_for('index'))

    termo_like = f"%{termo}%"

    if tipo_conta == 'profissional':
        # Profissional busca VAGAS
        vagas = Vaga.query.filter(
            (Vaga.titulo.ilike(termo_like)) | 
            (Vaga.descricao.ilike(termo_like)) | 
            (Vaga.requisitos.ilike(termo_like)) |
            (Vaga.local.ilike(termo_like))
        ).all()
        cards_filtrados = formatar_cards_vagas(vagas)
        
    elif tipo_conta == 'empresa':
        # Empresa busca PROFISSIONAIS
        profissionais = Profissional.query.filter(
            (Profissional.nome_profissional.ilike(termo_like)) |
            (Profissional.experiencia.ilike(termo_like)) |
            (Profissional.habilidades.ilike(termo_like)) |
            (Profissional.cidade.ilike(termo_like))
        ).all()
        cards_filtrados = formatar_cards_profissionais(profissionais)

    # 🟢 Retorna os resultados em formato JSON
    return jsonify(cards_filtrados)

@app.route('/index')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_login')) 
    
    tipo_conta = session.get('tipo_conta')
    cards = []
    titulo_secao = "Destaques" 

    if tipo_conta == 'profissional':
        vagas = Vaga.query.all() or []
        cards = formatar_cards_vagas(vagas) or []
        titulo_secao = "Vagas em Destaque"
        
    elif tipo_conta == 'empresa':
        perfis = Profissional.query.limit(50).all() or []
        cards = formatar_cards_profissionais(perfis) or []
        titulo_secao = "Profissionais Recentes"
        
        
    # Não passamos 'termo_pesquisa' aqui, apenas o conteúdo inicial
    return render_template('Index.html', tipo_conta=tipo_conta, cards=cards, titulo_secao=titulo_secao)

@app.route('/resultado_pesquisa')
def resultado_pesquisa():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_login')) 
    
    tipo_conta = session.get('tipo_conta')
    termo = request.args.get('search', '').strip() # Pega o termo da URL
    cards = []
    
    if not termo:
        # Correção: Retorne JSON vazio em vez de redirecionar
        return jsonify([])

    termo_like = f"%{termo}%"
    titulo_secao = f"Resultados da Pesquisa para '{termo}'"
    
    if tipo_conta == 'profissional':
        # Profissional busca VAGAS
        vagas = Vaga.query.filter(
            (Vaga.titulo.ilike(termo_like)) | 
            (Vaga.descricao.ilike(termo_like)) | 
            (Vaga.requisitos.ilike(termo_like)) |
            (Vaga.local.ilike(termo_like))
        ).all()
        cards = formatar_cards_vagas(vagas)
        
    elif tipo_conta == 'empresa':
        # Empresa busca PROFISSIONAIS
        profissionais = Profissional.query.filter(
            (Profissional.nome_profissional.ilike(termo_like)) |
            (Profissional.experiencia.ilike(termo_like)) |
            (Profissional.habilidades.ilike(termo_like)) |
            (Profissional.cidade.ilike(termo_like))
        ).all()
        cards = formatar_cards_profissionais(profissionais)

    # Renderiza o novo template com os resultados e o termo
    return render_template(
        'ResultadoPesquisa.html', 
        tipo_conta=tipo_conta, 
        cards=cards, 
        titulo_secao=titulo_secao, 
        termo_pesquisa=termo # Passa o termo para preencher o campo de busca
    )

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    nome = data.get('nome', '')
    tipo_conta = data.get('tipo_conta')
    endereco = data.get('endereco', '')
    cidade = data.get('cidade', '')
    estado = data.get('estado', '')
    cep = data.get('cep', '')

    if not all([email, senha, nome, tipo_conta]):
        return jsonify({"error": "Email, senha, nome e tipo de conta são obrigatórios"}), 400

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

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        if tipo_conta == 'profissional':
            novo_perfil = Profissional(
                 usuario_id=novo_usuario.id,
                 nome_profissional=nome,
                 endereco=endereco,
                 cidade=cidade,
                 estado=estado,
                 cep=cep
            )
        elif tipo_conta == 'empresa':
             novo_perfil = Empresa(
                usuario_id=novo_usuario.id,
                nome_empresa=nome,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                cep=cep,
                cnpj=data.get('cnpj')
            )

        db.session.add(novo_perfil)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar perfil: {e}")
        return jsonify({"error": "Erro ao cadastrar."}), 500

    session['usuario_id'] = novo_usuario.id
    session['tipo_conta'] = novo_usuario.tipo_conta
    session['nome'] = novo_usuario.nome

    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        if not all ([email, senha]):
            return jsonify({"success": False, "error": "Todos os campos são obrigatórios"}), 400
       
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return jsonify({"success": False, "error": "E-mail ou senha incorretos"}), 401
        # Correção: O bcrypt precisa de bytes, use .encode('utf-8') em ambos
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            session['usuario_id'] = usuario.id
            session['tipo_conta'] = usuario.tipo_conta
            session['nome'] = usuario.nome
            # Retorna JSON de sucesso
            return jsonify({"success": True, "message": "Login realizado com sucesso!"}), 200
        else:
            # Retorna JSON de falha de senha
            return jsonify({"success": False, "error": "E-mail ou senha incorretos"}), 401

    except Exception as e:
        # Garante que qualquer erro do servidor (ex: erro de DB) retorne JSON 500
        print(f"Erro interno no login: {e}")
        return jsonify({"success": False, "error": "Erro interno do servidor. Tente novamente mais tarde."}), 500
@app.route('/api/login_google', methods=['POST'])
def login_google():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"success": False, "error": "E-mail é obrigatório"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"success": False, "error": "E-mail não encontrado."}), 404
    session['usuario_id'] = usuario.id
    session['tipo_conta'] = usuario.tipo_conta
    session['nome'] = usuario.nome

    return jsonify({"success": True, "message": "Login Google realizado com sucesso!"}), 200

@app.route('/api/verificar_email', methods=['POST'])
def verificar_email():
    try:
        data = request.get_json()
        # Pode falhar se o body for None
        if data is None:
            print("Erro 500: JSON request body is missing or malformed.")
            return jsonify({"error": "Corpo da requisição ausente ou malformado."}), 400
        email = data.get('email')
        
        if not email:
            print("Erro 500: E-mail não fornecido no JSON.")
            return jsonify({"error": "E-mail é obrigatório"}), 400
        # A falha provavelmente está nesta linha ou nas próximas se o DB estiver offline.
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:

            return jsonify({"exists": True, "tipo_conta": usuario.tipo_conta}), 200

        else:
            return jsonify({"exists": False}), 200

    except Exception as e:
        # Imprime o erro completo no console do servidor Flask
        print(f"ERRO CRÍTICO NA ROTA /api/verificar_email: {e}")
        # Retorna um JSON de erro 500 para o frontend
        return jsonify({"error": "Erro interno ao verificar e-mail. Consulte os logs do servidor."}), 500

@app.route('/api/criar_curriculo', methods=['POST'])
def api_curriculo():
    usuario_id = session.get('usuario_id')
    tipo_conta = session.get('tipo_conta')

    if not usuario_id or tipo_conta != 'profissional':
        return jsonify({"error": "Acesso negado."}), 403
    data = request.get_json()
    profissional = Profissional.query.filter_by(usuario_id=usuario_id).first()

    if not profissional:
        return jsonify({"error": "Profissional não encontrado."}), 404
   
    usuario = Usuario.query.get(usuario_id)

    try:
        usuario.nome = data.get('nome', usuario.nome)
        profissional.telefone = data.get('telefone', profissional.telefone)
        profissional.endereco = data.get('endereco', profissional.endereco)
        profissional.experiencia = data.get('experiencia', profissional.experiencia)
        profissional.habilidades = data.get('habilidades', profissional.habilidades)
        profissional.nome_profissional = data.get('nome_profissional', profissional.nome_profissional)

        db.session.commit()
        return jsonify({"message": "Currículo atualizado com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar currículo: {e}")
        return jsonify({"error": "Erro ao salvar currículo."}), 500

@app.route('/api/criar_empresa', methods=['POST'])

def criar_empresa():
    usuario_id = session.get('usuario_id')

    if not usuario_id or session.get('tipo_conta') != 'empresa':
        return jsonify({"error": "Acesso negado ou usuário não autenticado"}), 403
    data = request.get_json()
    empresa = Empresa.query.filter_by(usuario_id=usuario_id).first()

    if not empresa:
        return jsonify({"error": "Empresa não encontrada."}), 404

    try:
        empresa.nome_empresa = data.get('nome_empresa', empresa.nome_empresa)
        empresa.descricao = data.get('descricao', empresa.descricao)
        empresa.site = data.get('site', empresa.site)
        empresa.cnpj = data.get('cnpj', empresa.cnpj)

        db.session.commit()
        return jsonify({"message": "Perfil de empresa atualizado!"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar perfil de empresa: {e}")
        return jsonify({"error": "Erro ao atualizar perfil de empresa. "}), 500

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('tipo_conta', None)
    session.pop('nome', None)
    return redirect(url_for('inicio'))

@app.route('/meu_perfil', methods=['GET', 'POST'])
def meu_perfil():
    usuario_id = session.get('usuario_id')
    tipo_conta = session.get('tipo_conta')

    if not usuario_id:
        return redirect(url_for('mostrar_login'))
    
    if tipo_conta == 'profissional':
        perfil = Profissional.query.filter_by(usuario_id=usuario_id).first()
        return render_template('FormularioCurriculo.html', profissional=perfil)

    elif tipo_conta == 'empresa':
        empresa = Empresa.query.filter_by(usuario_id=usuario_id).first()
        return render_template('FormularioEmpresa.html', empresa=empresa)

    return redirect(url_for('index'))

@app.route('/criar_vaga', methods=['GET', 'POST'])
def criar_vaga():
    usuario_id = session.get('usuario_id')
    if not usuario_id or session.get('tipo_conta') != 'empresa':
        return jsonify({"error": "Acesso negado."}), 403

    if request.method == 'POST':
        empresa_id = Empresa.query.filter_by(usuario_id=usuario_id).first().id
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        requisitos = request.form.get('requisitos')
        local = request.form.get('local')

        if not all([titulo, descricao, requisitos, local]):
            return render_template('FormularioVaga.html', error="Preencha todos os campos.")

        nova_vaga = Vaga(
            empresa_id=empresa_id,
            titulo=titulo,
            descricao=descricao,
            requisitos=requisitos,
            local=local
        )
        try:
            db.session.add(nova_vaga)
            db.session.commit()
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar vaga: {e}")
            return render_template('FormularioVaga.html', error="Erro ao salvar a vaga.")
        
    return render_template('FormularioVaga.html')

@app.route('/criar_banco')
def criar_banco():
    db.create_all()
    return "Banco criado"

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        inicializar_dados_ficticios(app)
    app.run(debug=True,host='0.0.0.0', port=5000)