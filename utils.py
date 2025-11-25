from models import Vaga, Profissional, Empresa, Candidatura

class MockVaga:
    def __init__(self, titulo, descricao, requisitos, local, empresa):
        self.titulo = titulo
        self.descricao = descricao
        self.requisitos = requisitos
        self.local = local
        self.empresa = MockEmpresa(empresa)

class MockProfissional:
    def __init__(self, nome_profissional, experiencia, habilidades, cidade, telefone):
        self.nome_profissional = nome_profissional
        self.experiencia = experiencia
        self.habilidades = habilidades
        self.cidade = cidade
        self.telefone = telefone

class MockEmpresa:
    def __init__(self, nome_empresa):
        self.nome_empresa = nome_empresa

def formatar_cards_vagas(vagas):
    if vagas is None:
        return [] 
        
    cards_formatados = []
    for vaga in vagas:
        nome_empresa = vaga.empresa.nome_empresa if vaga.empresa else "Empresa Desconhecida"
        
        salario = getattr(vaga, 'salario', 'Não Informado')

        cards_formatados.append({
            'id': vaga.id,
            'titulo': vaga.titulo,
            'descricao': vaga.descricao,
            'detalhes': {
                'empresa': nome_empresa,
                'local': vaga.local,
                'requisitos': vaga.requisitos,
                'salario': salario,
            }
        })
    return cards_formatados


def formatar_cards_profissionais(profissionais):
    
    if profissionais is None:
        return [] 

    cards_formatados = []
    for perfil in profissionais:
        
        nome_usuario_fallback = getattr(perfil, 'usuario', None)
        nome_usuario = nome_usuario_fallback.nome if nome_usuario_fallback else "Profissional"
        nome_titulo = perfil.nome_profissional if perfil.nome_profissional else nome_usuario

        cards_formatados.append({
            'id': perfil.id,
            'titulo': nome_titulo, 
            'descricao': perfil.experiencia, 
            'detalhes': {
                'experiencia': perfil.experiencia,
                'habilidades': perfil.habilidades,
                'telefone': perfil.telefone,
                'cidade': perfil.cidade, 
            }
        })
    return cards_formatados