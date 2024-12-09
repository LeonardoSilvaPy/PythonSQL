from src.db.connection import engine
from src.db.model import Usuario  # Importe o modelo Usuario

# Cria todas as tabelas definidas nos modelos
def criar_tabelas():
    Usuario.metadata.create_all(bind=engine)  # Cria a tabela no banco de dados

# Chama a função para criar a tabela
if __name__ == '__main__':
    criar_tabelas()
    print("Tabelas criadas com sucesso!")
