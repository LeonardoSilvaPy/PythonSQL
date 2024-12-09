# src/db/model.py
import traceback
from cgitb import text
from importlib.metadata import metadata
from msilib import Table
import sys

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, Time

from src.db import connection
from src.db.connection import Session, Base, engine


# Definindo a classe de agendamento
class Agendamento(Base):
    __tablename__ = 'agendamentos'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String(100), nullable=False)
    cpf = mapped_column(String(11), nullable=False)
    servico = mapped_column(String(100), nullable=False)
    contato = mapped_column(String(20), nullable=False)
    local = mapped_column(String(100), nullable=False)
    data = mapped_column(Date, nullable=False)
    hora = mapped_column(Time, nullable=False)

    def __repr__(self):
        return (f"Agendamento(id={self.id}, nome={self.nome}, cpf={self.cpf}, "
                f"servico={self.servico}, contato={self.contato}, "
                f"local={self.local}, data={self.data}, hora={self.hora})")


def insert_agendamento(nome, cpf, servico, contato, local, data, hora):
    session = Session()
    try:
        # Criação do novo agendamento
        novo_agendamento = Agendamento(
            nome=nome, cpf=cpf, servico=servico,
            contato=contato, local=local, data=data, hora=hora
        )

        # Adiciona o novo agendamento à sessão
        session.add(novo_agendamento)

        # Salva as mudanças
        session.commit()
        print(f"Agendamento para {nome} inserido com sucesso!")
    except IntegrityError as e:
        print(f"Erro de integridade: {e}")
        session.rollback()
    except Exception as e:
        print(f"Erro ao inserir agendamento: {e}")
        session.rollback()
    finally:
        session.close()


def get_agendamentos(cpf):
    session = Session()
    try:
        # Consulta os agendamentos filtrados pelo CPF
        agendamentos = session.query(Agendamento).filter(Agendamento.cpf == cpf).all()
        return agendamentos
    except Exception as e:
        print(f"Erro ao buscar agendamentos para o CPF {cpf}: {e}")
        return []
    finally:
        session.close()


# Definindo a classe do usuário
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String(100), nullable=False)
    email = mapped_column(String(100), nullable=False, unique=True)
    senha = mapped_column(String(100), nullable=False)
    cpf = mapped_column(String(11), nullable=False, unique=True)
    contato = mapped_column(String(15), nullable=False)


    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, email={self.email})"


def drop_users_table():
    session = Session()  # Cria uma nova sessão
    try:
        # Executando o comando DROP TABLE diretamente na conexão, usando text()
        session.execute(text("DROP TABLE IF EXISTS usuarios"))
        print("Tabela 'usuarios' excluída com sucesso!")
    except Exception as e:
        # Exibe a exceção diretamente
        print(f"Erro ao excluir a tabela: {e}")
        # Captura e imprime o traceback completo do erro
        traceback.print_exc()
    finally:
        # Fecha a sessão
        session.close()

def insert_user(nome, email, senha, cpf, contato):
    session = Session()  # Cria uma nova sessão

    try:
        # Criação do novo usuário com os novos campos
        new_user = Usuario(nome=nome, email=email, senha=senha, cpf=cpf, contato=contato)

        # Adiciona o novo usuário à sessão
        session.add(new_user)

        # Salva as mudanças
        session.commit()
        print(f"Usuário {nome} inserido com sucesso!")
    except IntegrityError as e:
        print(f"Erro de integridade: {e}")
        session.rollback()
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        session.rollback()
    finally:
        # Fecha a sessão
        session.close()


def list_users():
    session = Session()  # Cria uma nova sessão
    try:
        # Consulta todos os usuários
        usuarios = session.query(Usuario).all()

        # Retorna a lista de usuários
        return usuarios
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        # Fecha a sessão
        session.close()


def update_user(user_id, nome=None, email=None, senha=None, cpf=None, contato=None):
    session = Session()  # Cria uma nova sessão

    try:
        # Obtém o usuário pelo ID
        usuario = session.query(Usuario).filter_by(id=user_id).first()

        if not usuario:
            print(f"Usuário com ID {user_id} não encontrado.")
            return

        # Atualiza os campos informados
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.senha = senha
        if cpf:
            usuario.cpf = cpf
        if contato:
            usuario.contato = contato

        # Salva as mudanças
        session.commit()
        print(f"Usuário com ID {user_id} atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        session.rollback()
    finally:
        # Fecha a sessão
        session.close()


def get_user_by_email(email):
    session = Session()  # Cria uma nova sessão
    try:
        # Busca o usuário pelo email
        usuario = session.query(Usuario).filter_by(email=email).first()

        if usuario:
            return usuario
        else:
            print(f"Usuário com email '{email}' não encontrado.")
            return None
    except Exception as e:
        print(f"Erro ao buscar usuário por email: {e}")
        return None
    finally:
        # Fecha a sessão
        session.close()

def delete_user(user_id):
    session = Session()  # Cria uma nova sessão
    try:
        # Busca o usuário pelo ID
        usuario = session.query(Usuario).filter_by(id=user_id).first()

        if not usuario:
            print(f"Usuário com ID {user_id} não encontrado.")
            return

        # Remove o usuário
        session.delete(usuario)
        session.commit()
        print(f"Usuário com ID {user_id} deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        session.rollback()
    finally:
        # Fecha a sessão
        session.close()

def login_user(email, senha):
    session = Session()  # Cria uma nova sessão
    try:
        # Busca o usuário pelo email e senha
        usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()

        if usuario:
            print(f"Login bem-sucedido para o usuário: {usuario.nome}")
            return usuario
        else:
            print("Email ou senha inválidos.")
            return None
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None
    finally:
        # Fecha a sessão
        session.close()
