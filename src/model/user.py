from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
from src.db.connection import Base

class Usuario(Base):
    __tablename__ = 'usuarios'  # Nome da tabela no banco de dados

    id = mapped_column(Integer, primary_key=True, autoincrement=True)  # ID do usuário, chave primária
    nome = mapped_column(String(100), nullable=False)  # Nome do usuário
    email = mapped_column(String(100), nullable=False, unique=True)  # Email do usuário, único
    senha = mapped_column(String(100), nullable=False)  # Senha do usuário

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, email={self.email})"