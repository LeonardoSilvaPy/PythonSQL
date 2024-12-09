from flask import Flask, request, jsonify
from src.db.model import insert_user
from src.db.model import login_user
from src.db.model import insert_agendamento, get_agendamentos


app = Flask(__name__)

@app.route('/cadastro', methods=['POST'])
def cadastro():
    # Recebe os dados do corpo da requisição
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    cpf = data.get('cpf')
    contato = data.get('contato')

    # Validação dos campos obrigatórios
    if not nome or not email or not senha or not cpf or not contato:
        return jsonify({"message": "Nome, email, senha, CPF e contato são obrigatórios"}), 404

    # Validação básica do CPF
    if len(cpf) != 11 or not cpf.isdigit():
        return jsonify({"message": "CPF inválido. Deve conter 11 dígitos numéricos."}), 404

    # Validação básica do contato
    if len(contato) < 10 or not contato.isdigit():
        return jsonify({"message": "Contato inválido. Deve conter pelo menos 10 dígitos numéricos."}), 404

    try:
        # Insere o novo usuário
        insert_user(nome, email, senha, cpf, contato)
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar usuário: {e}"}), 500

if __name__ == '__main__':

    @app.route('/login', methods=['POST'])
    def login():
        # Recebe as credenciais do corpo da requisição
        data = request.json
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({"message": "Email e senha são obrigatórios"}), 404

        # Tenta fazer login
        usuario = login_user(email, senha)

        if usuario:
            return jsonify({
                "message": "Login bem-sucedido",
                "user": {
                    "cpf": usuario.cpf,
                    "nome": usuario.nome,
                    "email": usuario.email
                }
            }), 200
        else:
            return jsonify({"message": "Credenciais inválidas"}), 401

    @app.route('/agendamentos', methods=['POST'])
    def criar_agendamento():
        data = request.json
        nome = data.get('nome')
        cpf = data.get('cpf')
        servico = data.get('servico')
        contato = data.get('contato')
        local = data.get('local')
        data_agendamento = data.get('data')  # Formato: YYYY-MM-DD
        hora_agendamento = data.get('hora')  # Formato: HH:MM:SS

        if not all([nome, cpf, servico, contato, local, data_agendamento, hora_agendamento]):
            return jsonify({"message": "Todos os campos são obrigatórios"}), 404

        try:
            insert_agendamento(nome, cpf, servico, contato, local, data_agendamento, hora_agendamento)
            return jsonify({"message": "Agendamento criado com sucesso!"}), 201
        except Exception as e:
            return jsonify({"message": f"Erro ao criar agendamento: {e}"}), 500


    @app.route('/agendamentos', methods=['GET'])
    def listar_agendamentos():
        cpf = request.args.get('cpf')

        if not cpf:
            return jsonify({"message": "CPF é obrigatório para listar agendamentos"}), 400

        try:
            agendamentos = get_agendamentos(cpf)  # Função para buscar agendamentos filtrados pelo CPF
            return jsonify([{
                "id": agendamento.id,
                "nome": agendamento.nome,
                "cpf": agendamento.cpf,
                "servico": agendamento.servico,
                "contato": agendamento.contato,
                "local": agendamento.local,
                "data": str(agendamento.data),
                "hora": str(agendamento.hora)
            } for agendamento in agendamentos]), 200
        except Exception as e:
            return jsonify({"message": f"Erro ao buscar agendamentos: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
