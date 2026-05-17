from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

# Liberação de CORS para aceitar conexões locais de arquivos (file://)
CORS(app, resources={r"/*": {"origins": "*"}})

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # <--- COLOQUE A SUA SENHA DO WORKBENCH AQUI!
        database="estoque_hospitalar"
    )

# Força os cabeçalhos de liberação em todas as respostas do servidor
@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

# Rota para listar o estoque real
@app.route('/estoque', methods=['GET'])
def listar_estoque():
    conexao = conectar_banco()
    mensageiro = conexao.cursor(dictionary=True)
    mensageiro.execute("SELECT codigo_qr, nome, quantidade FROM acessorios")
    lista_produtos = mensageiro.fetchall()
    mensageiro.close()
    conexao.close()
    return jsonify(lista_produtos), 200

# Rota de dar baixa (Saída)
@app.route('/baixa', methods=['POST'])
def dar_baixa():
    dados = request.get_json()
    codigo_lido = dados.get('codigo')
    
    conexao = conectar_banco()
    mensageiro = conexao.cursor()
    
    mensageiro.execute("SELECT nome FROM acessorios WHERE codigo_qr = %s", (codigo_lido,))
    produto = mensageiro.fetchone()
    
    if not produto:
        mensageiro.close()
        conexao.close()
        return jsonify({"status": "erro", "mensagem": "Item não cadastrado no banco."}), 400
        
    nome_produto = produto[0]
    
    # COMANDO CORRIGIDO: quantidade = quantidade - 1
    ordem = "UPDATE acessorios SET quantidade = quantidade - 1 WHERE codigo_qr = %s AND quantidade > 0"
    mensageiro.execute(ordem, (codigo_lido,))
    conexao.commit()
    
    linhas_afetadas = mensageiro.rowcount
    mensageiro.close()
    conexao.close()
    
    if linhas_afetadas > 0:
        return jsonify({"status": "sucesso", "nome": nome_produto, "mensagem": "unidade retirada!"}), 200
    else:
        return jsonify({"status": "erro", "mensagem": f"{nome_produto} está com estoque zerado!"}), 400

# Rota para dar Entrada (Soma itens existentes)
@app.route('/entrada', methods=['POST'])
def dar_entrada():
    dados = request.get_json()
    codigo_lido = dados.get('codigo')
    qtd_nova = int(dados.get('quantidade', 1))
    
    conexao = conectar_banco()
    mensageiro = conexao.cursor()
    
    mensageiro.execute("SELECT nome FROM acessorios WHERE codigo_qr = %s", (codigo_lido,))
    produto = mensageiro.fetchone()
    
    if not produto:
        mensageiro.close()
        conexao.close()
        return jsonify({"status": "erro", "mensagem": "Código não encontrado. Cadastre o item primeiro."}), 400
        
    nome_produto = produto[0]
    
    ordem = "UPDATE acessorios SET quantidade = quantidade + %s WHERE codigo_qr = %s"
    mensageiro.execute(ordem, (qtd_nova, codigo_lido))
    conexao.commit()
    
    mensageiro.close()
    conexao.close()
    return jsonify({"status": "sucesso", "nome": nome_produto, "mensagem": f"{qtd_nova} unidades adicionadas!"}), 200

# Rota de Cadastro Padronizado
@app.route('/cadastrar', methods=['POST'])
def cadastrar_produto():
    dados = request.get_json()
    codigo_lido = dados.get('codigo')
    tipo = dados.get('tipo')
    marca = dados.get('marca')
    especificacao = dados.get('especificacao')
    qtd_inicial = int(dados.get('quantidade', 0))
    
    # Monta o nome seguindo o padrão oficial da Engenharia Clínica
    nome_padronizado = f"{tipo.upper()} {marca.upper()}"
    if especificacao:
        nome_padronizado += f" - {especificacao.upper()}"
    
    conexao = conectar_banco()
    mensageiro = conexao.cursor()
    
    mensageiro.execute("SELECT codigo_qr FROM acessorios WHERE codigo_qr = %s", (codigo_lido,))
    if mensageiro.fetchone():
        mensageiro.close()
        conexao.close()
        return jsonify({"status": "erro", "mensagem": "Este código QR já está cadastrado!"}), 400
        
    ordem = "INSERT INTO acessorios (codigo_qr, nome, quantidade) VALUES (%s, %s, %s)"
    mensageiro.execute(ordem, (codigo_lido, nome_padronizado, qtd_inicial))
    conexao.commit()
    
    mensageiro.close()
    conexao.close()
    return jsonify({"status": "sucesso", "mensagem": f"Item '{nome_padronizado}' cadastrado no padrão!"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)