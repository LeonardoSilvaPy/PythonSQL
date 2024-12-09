# src/main.py
from src.db.connection import init_db, Session
from src.db.model import insert_user, list_users, update_user, get_user_by_email, delete_user, Usuario, drop_users_table
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


# Inicializa o banco de dados (sem app)
init_db()

if __name__ == '__main__':

    # Chama a função de inserção diretamente
    #insert_user('Gabi3f', 'gabi3f@email.com', '33313f', '12345678902','11987654321')
    #print("Usuário inserido com sucesso!")

    # Lista todos os usuários
    #usuarios = list_users()
    #print("Usuários cadastrados:")
    #for usuario in usuarios:
        #print(usuario)

    #update_user(user_id=1, nome="Gabi Atualizada", email="gabi_novo@email.com", senha="nova_senha", cpf="98765432100",contato="11912345678")

    # Atualiza o usuário com ID 5
    #user_id_to_update = 0
    #update_user(user_id_to_update, nome="Gabriela", email="gabriela2@email.com", senha="nova_senha123")

    # Busca um usuário pelo email
    #email_procurado = 'gabi@email.com'
    #usuario = get_user_by_email(email_procurado)
    #if usuario:
        #print(f"Usuário encontrado: {usuario}")
    #else:
        #print(f"Usuário com email '{email_procurado}' não foi encontrado.")

    # Deleta o usuário pelo id
    #if usuarios:
        #user_id_to_delete = 0
        #delete_user(user_id_to_delete)


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