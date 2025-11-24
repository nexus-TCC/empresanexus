from models import Vaga, Profissional, Empresa
from cards import Card, criar_card_vaga, criar_card_profissional, criar_card_empresa

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
# Remova estas classes Mock quando seus modelos reais estiverem importados.

# Exemplo de importação real (se você tiver um arquivo models.py):
# from .models import Vaga, Profissional, Empresa
def formatar_cards_vagas(vagas):
    """Formata uma lista de objetos Vaga em dicionários para exibição nos cards."""
    cards_formatados = []
    for vaga in vagas:
        # Busca o nome da empresa através do relacionamento
        nome_empresa = vaga.empresa.nome_empresa if vaga.empresa else "Empresa Desconhecida"
        
        cards_formatados.append({
            'id': vaga.id,
            'titulo': vaga.titulo,
            'descricao': vaga.descricao,
            'detalhes': {
                'empresa': nome_empresa,
                'local': vaga.local,
                'requisitos': vaga.requisitos,
                'salario': vaga.salario,
            }
        })
    return cards_formatados

def formatar_cards_profissionais(profissionais):
    """
    Formata uma lista de objetos Profissional em dicionários para exibição nos cards,
    incluindo a cidade para a pesquisa.
    """
    cards_formatados = []
    for perfil in profissionais:
        # Usa o nome do profissional ou o nome do usuário como fallback
        nome_titulo = perfil.nome_profissional if perfil.nome_profissional else (perfil.usuario.nome if perfil.usuario else "Profissional")

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
