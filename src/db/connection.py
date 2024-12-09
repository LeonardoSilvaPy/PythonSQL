# src/db/connection.py
import urllib.parse  # Adicione esta linha para corrigir o erro

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurações do banco de dados
DATABASE_HOST = 'autorack.proxy.rlwy.net'
DATABASE_PORT = '25586'
DATABASE_NAME = 'railway'
DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = 'RhECSoYuzufDsyfKcOFeBcBDiimphBkk'

DATABASE_PASSWORD_ESCAPED = urllib.parse.quote_plus(DATABASE_PASSWORD)

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD_ESCAPED}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Criação da engine de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Classe base para os modelos
Base = declarative_base()

# Session maker
Session = sessionmaker(bind=engine)

# Função de inicialização (sem app)
def init_db():
    Base.metadata.create_all(engine)  # Cria as tabelas no banco
    print("Banco de dados inicializado com sucesso!")
