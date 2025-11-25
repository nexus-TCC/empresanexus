from flask import Flask, render_template, request, jsonify, redirect, url_for, session, abort, flash
from db import db
from models import Usuario, Profissional, Empresa, Vaga, Candidatura
from utils import formatar_cards_vagas, formatar_cards_profissionais
import bcrypt
import os

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'AcabaPeloAmorDeDeus'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o Flask-SQLAlchemy
db.init_app(app)

# Filtro customizado para truncar strings no template Jinja2
def truncate_filter(s, length=255, killwords=False, end='...'):
    # CORREÇÃO: Garante que 's' é uma string antes de chamar len()
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s) # Converte para string caso seja um número, etc.
        
    if len(s) <= length:
        return s
    
    if killwords:
        return s[:length] + end
    
    words = s.split(' ')
    result = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(result) > length:
            break
        result.append(word)
        current_length += len(word)
    
    return ' '.join(result) + end

# Registra o filtro no ambiente Jinja2 do Flask
app.jinja_env.filters['truncate'] = truncate_filter


@app.after_request
def add_security_headers(response):
    #response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    #response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
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
        
        # 1. Usuários
        usuario_admin = Usuario(nome='Admin Nexus', email=ADMIN_EMAIL, senha=admin_senha_hash, tipo_conta='empresa')
        usuario_profissional = Usuario(nome='Ana Curriculo', email='ana@curriculo.com', senha=profissional_senha_hash, tipo_conta='profissional')

        db.session.add_all([usuario_admin, usuario_profissional])
        db.session.commit()
        
        # 2. Perfis
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
        
        # 3. Vagas
        vaga_1 = Vaga(
            empresa_id=empresa_admin.id,
            titulo='Analista de QA Pleno (Híbrido)',
            descricao='Vaga para garantir a qualidade de nossos produtos digitais, focando em testes de regressão e performance.',
            requisitos='Mínimo 3 anos de experiência em QA. Conhecimento em metodologias ágeis.',
            local='São Paulo / Híbrido'
        )
        vaga_2 = Vaga(
            empresa_id=empresa_admin.id,
            titulo='Desenvolvedor Python Júnior',
            descricao='Buscamos programador Python com foco em web development.',
            requisitos='Python, Flask ou Django, SQL. Inglês básico.',
            local='Remoto'
        )
        db.session.add_all([vaga_1, vaga_2])
        db.session.commit()
        
        # 4. Candidaturas (Para teste) <--- INCLUSÃO
        candidatura_teste = Candidatura(vaga_id=vaga_1.id, profissional_id=profissional_ana.id, status='Visualizada')
        db.session.add(candidatura_teste)
        db.session.commit()
        
        print("Dados fictícios mínimos criados com sucesso!")
        
# ------------------ ROTAS DE NAVEGAÇÃO ------------------

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
        return jsonify([])

    termo_like = f"%{termo}%"

    if tipo_conta == 'profissional':
        vagas = Vaga.query.filter(
            (Vaga.titulo.ilike(termo_like)) | 
            (Vaga.descricao.ilike(termo_like)) | 
            (Vaga.requisitos.ilike(termo_like)) |
            (Vaga.local.ilike(termo_like))
        ).all()
        cards_filtrados = formatar_cards_vagas(vagas)
        
    elif tipo_conta == 'empresa':
        profissionais = Profissional.query.filter(
            (Profissional.nome_profissional.ilike(termo_like)) |
            (Profissional.experiencia.ilike(termo_like)) |
            (Profissional.habilidades.ilike(termo_like)) |
            (Profissional.cidade.ilike(termo_like))
        ).all()
        cards_filtrados = formatar_cards_profissionais(profissionais)

    return jsonify(cards_filtrados)


@app.route('/index')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_login')) 
    
    tipo_conta = session.get('tipo_conta')
    cards = []
    titulo_secao = "Destaques" 

    if tipo_conta == 'profissional':
        vagas = Vaga.query.order_by(Vaga.id.desc()).limit(10).all() 
        cards = formatar_cards_vagas(vagas) or [] 
        titulo_secao = "Vagas em Destaque"
        
    elif tipo_conta == 'empresa':
        perfis = Profissional.query.order_by(Profissional.id.desc()).limit(10).all() 
        cards = formatar_cards_profissionais(perfis) or [] 
        titulo_secao = "Profissionais Recentes"
        
    if cards is None:
        print("ALERTA: 'cards' é None! Forçando para lista vazia.")
        cards = []
        
    return render_template('Index.html', tipo_conta=tipo_conta, cards=cards, titulo_secao=titulo_secao, termo_pesquisa='')

@app.route('/resultado_pesquisa')
def resultado_pesquisa():
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_login')) 
    
    tipo_conta = session.get('tipo_conta')
    termo = request.args.get('search', '').strip()

    if not termo:
        return redirect(url_for('index'))

    termo_like = f"%{termo}%"
    titulo_secao = f"Resultados da Pesquisa para '{termo}'"
    cards = []
    
    if tipo_conta == 'profissional':
        vagas = Vaga.query.filter(
            (Vaga.titulo.ilike(termo_like)) | 
            (Vaga.descricao.ilike(termo_like)) | 
            (Vaga.requisitos.ilike(termo_like)) |
            (Vaga.local.ilike(termo_like))
        ).all()
        cards = formatar_cards_vagas(vagas)
        
    elif tipo_conta == 'empresa':
        profissionais = Profissional.query.filter(
            (Profissional.nome_profissional.ilike(termo_like)) |
            (Profissional.experiencia.ilike(termo_like)) |
            (Profissional.habilidades.ilike(termo_like)) |
            (Profissional.cidade.ilike(termo_like))
        ).all()
        cards = formatar_cards_profissionais(profissionais)

    return render_template(
        'ResultadoPesquisa.html', 
        tipo_conta=tipo_conta, 
        cards=cards, 
        titulo_secao=titulo_secao, 
        termo_pesquisa=termo 
    )

@app.route('/detalhe/<string:tipo>/<int:id>')
def detalhe(tipo, id):
    if 'usuario_id' not in session:
        return redirect(url_for('mostrar_login'))

    item = None
    template_name = ''
    
    if tipo == 'vaga':
        item = Vaga.query.get_or_404(id)
        template_name = 'DetalheVaga.html'
    elif tipo == 'profissional':
        item = Profissional.query.get_or_404(id)
        template_name = 'DetalheProfissional.html'
    else:
        return redirect(url_for('index'))

    # Variáveis de Candidatura (para DetalheVaga) <--- CORRIGIDO
    ja_candidatou = False
    sucesso = request.args.get('sucesso')
    erro = request.args.get('erro')

    if tipo == 'vaga' and session.get('tipo_conta') == 'profissional':
        profissional = Profissional.query.filter_by(usuario_id=session['usuario_id']).first()
        if profissional:
            ja_candidatou = Candidatura.query.filter_by(
                vaga_id=id, 
                profissional_id=profissional.id
            ).first() is not None
            
    return render_template(
        template_name,
        item=item,
        tipo_conta=session.get('tipo_conta'),
        ja_candidatou=ja_candidatou,
        sucesso=sucesso,
        erro=erro
    )

# ------------------ ROTAS DE CANDIDATURA ------------------

@app.route('/candidatar/<int:vaga_id>', methods=['POST', 'GET'])
def candidatar(vaga_id):
    if session.get('tipo_conta') != 'profissional':
        flash('Acesso negado. Apenas profissionais podem se candidatar.', 'error')
        return redirect(url_for('index'))
    
    profissional = Profissional.query.filter_by(usuario_id=session['usuario_id']).first()
    vaga = Vaga.query.get(vaga_id)
    
    if not profissional or not vaga:
        flash("Erro: Vaga ou perfil não encontrado.", 'error')
        return redirect(url_for('detalhe', tipo='vaga', id=vaga_id))

    try:
        nova_candidatura = Candidatura(vaga_id=vaga_id, profissional_id=profissional.id)
        db.session.add(nova_candidatura)
        db.session.commit()
        
        # MENSAGEM DE SUCESSO
        flash("Sua candidatura foi enviada com sucesso!", 'success')
        return redirect(url_for('detalhe', tipo='vaga', id=vaga_id))
        
    except Exception as e:
        db.session.rollback()
        # Captura o erro de UniqueConstraint (candidatura duplicada)
        if 'UNIQUE constraint failed' in str(e):
            # MENSAGEM DE ERRO (DUPLICADA)
            flash("Você já se candidatou a esta vaga.", 'warning')
        else:
            print(f"Erro ao candidatar: {e}")
            # MENSAGEM DE ERRO GERAL
            flash("Erro ao candidatar: Tente novamente mais tarde.", 'error')
            
        return redirect(url_for('detalhe', tipo='vaga', id=vaga_id))


@app.route('/minhas-candidaturas')
def minhas_candidaturas():
    if session.get('tipo_conta') != 'profissional':
        return redirect(url_for('index'))

    profissional = Profissional.query.filter_by(usuario_id=session['usuario_id']).first()
    
    if not profissional:
        return redirect(url_for('index'))

    vagas_candidatadas = Vaga.query.join(Candidatura).filter(
        Candidatura.profissional_id == profissional.id
    ).all()

    cards = formatar_cards_vagas(vagas_candidatadas)

    return render_template(
        'VagasCandidatos.html',
        cards=cards,
        tipo_conta='profissional',
        titulo_secao="Minhas Candidaturas"
    )

@app.route('/minhas-vagas')
def minhas_vagas():
    if session.get('tipo_conta') != 'empresa':
        return redirect(url_for('index'))

    empresa = Empresa.query.filter_by(usuario_id=session['usuario_id']).first()
    
    if not empresa:
        return redirect(url_for('index'))
        
    vagas_anunciadas = Vaga.query.filter_by(empresa_id=empresa.id).all()
    
    vagas_com_candidatos = []
    for vaga in vagas_anunciadas:
        vagas_com_candidatos.append({
            'vaga': vaga,
            'num_candidatos': Candidatura.query.filter_by(vaga_id=vaga.id).count() 
        })
    
    return render_template(
        'AcompanhamentoVagas.html',
        vagas_data=vagas_com_candidatos,
        tipo_conta='empresa'
    )

@app.route('/vaga/<int:vaga_id>/candidatos')
def candidatos_por_vaga(vaga_id):
    if session.get('tipo_conta') != 'empresa':
        return redirect(url_for('index'))
        
    vaga = Vaga.query.get_or_404(vaga_id)
    
    empresa = Empresa.query.filter_by(usuario_id=session['usuario_id']).first()
    if vaga.empresa_id != empresa.id:
        # A empresa não é dona da vaga, acesso negado
        abort(403) 
    
    candidaturas = Candidatura.query.filter_by(vaga_id=vaga_id).all()
    
    candidatos = []
    for c in candidaturas:
        candidato_perfil = Profissional.query.get(c.profissional_id)
        candidatos.append({
            'perfil': candidato_perfil,
            'candidatura_id': c.id, # Adicionado ID da candidatura para a API de status
            'data_candidatura': c.data_candidatura,
            'status': c.status
        })
    
    # Lista de status possíveis para o dropdown no frontend
    status_possiveis = ['Pendente', 'Visualizada', 'Em Entrevista', 'Aprovado', 'Rejeitado']
    
    return render_template(
        'CandidatosVaga.html', # Você precisará atualizar este template
        vaga=vaga,
        candidatos=candidatos,
        tipo_conta='empresa',
        status_possiveis=status_possiveis
    )


# ROTA NOVA: API para a Empresa atualizar o status do candidato
@app.route('/api/atualizar_status_candidatura', methods=['POST'])
def api_atualizar_status_candidatura():
    # 1. Verificação de Autenticação e Tipo
    if session.get('tipo_conta') != 'empresa':
        return jsonify({"success": False, "error": "Acesso negado. Apenas empresas podem alterar o status."}), 403
    
    usuario_id = session.get('usuario_id')
    data = request.get_json()
    
    candidatura_id = data.get('candidatura_id')
    novo_status = data.get('novo_status')
    
    if not all([candidatura_id, novo_status]):
        return jsonify({"success": False, "error": "ID da candidatura e novo status são obrigatórios."}), 400

    try:
        # 2. Encontra a Candidatura
        candidatura = Candidatura.query.get(candidatura_id)
        if not candidatura:
            return jsonify({"success": False, "error": "Candidatura não encontrada."}), 404

        # 3. Verifica a Propriedade da Vaga
        vaga = Vaga.query.get(candidatura.vaga_id)
        empresa = Empresa.query.filter_by(usuario_id=usuario_id).first()
        
        # Garante que a empresa logada é a dona da vaga
        if not empresa or vaga.empresa_id != empresa.id:
            return jsonify({"success": False, "error": "Você não tem permissão para gerenciar esta candidatura."}), 403

        # 4. Atualiza o Status
        candidatura.status = novo_status
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": "Status da candidatura atualizado com sucesso!",
            "novo_status": novo_status
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar status da candidatura: {e}")
        return jsonify({"success": False, "error": "Erro interno ao atualizar o status."}), 500

# ------------------ ROTAS DE AUTENTICAÇÃO E PERFIL (ORIGINAIS) ------------------

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
        
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            session['usuario_id'] = usuario.id
            session['tipo_conta'] = usuario.tipo_conta
            session['nome'] = usuario.nome

            return jsonify({"success": True, "message": "Login realizado com sucesso!"}), 200
        else:
            return jsonify({"success": False, "error": "E-mail ou senha incorretos"}), 401

    except Exception as e:
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
        if data is None:
            return jsonify({"error": "Corpo da requisição ausente ou malformado."}), 400
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "E-mail é obrigatório"}), 400
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            return jsonify({"exists": True, "tipo_conta": usuario.tipo_conta}), 200
        else:
            return jsonify({"exists": False}), 200

    except Exception as e:
        print(f"ERRO CRÍTICO NA ROTA /api/verificar_email: {e}")
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
    flash("Você foi desconectado com sucesso. Volte sempre!", 'info')
    return redirect(url_for('inicio'))

@app.route('/meu_perfil', methods=['GET', 'POST'])
def meu_perfil():
    usuario_id = session.get('usuario_id')
    tipo_conta = session.get('tipo_conta')

    if not usuario_id:
        return redirect(url_for('mostrar_login'))
    
    if tipo_conta == 'profissional':
        perfil = Profissional.query.filter_by(usuario_id=usuario_id).first()
        if perfil is None:
            return redirect(url_for('index'))
        return render_template('FormularioCurriculo.html', profissional=perfil)

    elif tipo_conta == 'empresa':
        empresa = Empresa.query.filter_by(usuario_id=usuario_id).first()
        if empresa is None:
            return redirect(url_for('index'))
        return render_template('FormularioEmpresa.html', empresa=empresa)

    return redirect(url_for('index'))

@app.route('/criar_vaga', methods=['POST', 'GET'])
def criar_vaga():
    usuario_id = session.get('usuario_id')
    if not usuario_id or session.get('tipo_conta') != 'empresa':
        flash('Acesso negado. Apenas empresas podem criar vagas.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        empresa = Empresa.query.filter_by(usuario_id=usuario_id).first()
        if not empresa:
            flash('Erro ao encontrar perfil da empresa.', 'error')
            return redirect(url_for('index'))
            
        empresa_id = empresa.id
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        requisitos = request.form.get('requisitos')
        local = request.form.get('local')

        if not all([titulo, descricao, requisitos, local]):
            flash("Preencha todos os campos obrigatórios.", 'warning')
            return render_template('FormularioVaga.html')

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
            
            # MENSAGEM DE SUCESSO
            flash(f"Vaga '{titulo}' publicada com sucesso!", 'success')
            return redirect(url_for('minhas_vagas'))
        
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar vaga: {e}")
            # MENSAGEM DE ERRO GERAL
            flash("Erro ao salvar a vaga. Tente novamente.", 'error')
            return render_template('FormularioVaga.html')
        
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