from db import db
from models import Usuario, Profissional, Empresa, Vaga
 
class Card:
    def __init__(self, id, titulo, descricao, detalhes):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.detalhes = detalhes
 
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'detalhes': self.detalhes
        }
def criar_card_vaga(vaga):
    detalhes = {
        'requisitos': vaga.requisitos,
        'local': vaga.local,
        'empresa': vaga.empresa.nome_empresa
    }
    return Card(
        id=vaga.id,
        titulo=vaga.titulo,
        descricao=vaga.descricao,
        detalhes=detalhes
    )
def criar_card_profissional(profissional):
    detalhes = {
        'telefone': profissional.telefone,
        'endereco': profissional.endereco,
        'experiencia': profissional.experiencia,
        'habilidades': profissional.habilidades
    }
    return Card(
        id=profissional.id,
        titulo=profissional.nome_profissional,
        descricao=f" {profissional.cidade}, {profissional.estado}",
        detalhes=detalhes
    )
def criar_card_empresa(empresa):
    detalhes = {
        'descricao': empresa.descricao,
        'site': empresa.site,
        'cnpj': empresa.cnpj
    }
    return Card(
        id=empresa.id,
        titulo=empresa.nome_empresa,
        descricao=f"{empresa.cidade}, {empresa.estado}",
        detalhes=detalhes
    )