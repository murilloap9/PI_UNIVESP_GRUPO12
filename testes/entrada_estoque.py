import mysql.connector

# Abrindo o cofre
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456", # Coloque a sua senha aqui
    database="estoque_hospitalar"
)

mensageiro = conexao.cursor()

# 1. O sistema pergunta qual é a etiqueta e quantas peças chegaram
codigo_lido = input("Qual é o código QR da peça que chegou? ")
quantidade_nova = int(input("Quantas unidades chegaram? "))

# 2. A regra de soma: ele encontra o item certo e soma a quantidade nova com a antiga
ordem_somar = "UPDATE acessorios SET quantidade = quantidade + %s WHERE codigo_qr = %s"

# Colocamos os valores na ordem certa (primeiro a quantidade, depois o código)
valores = (quantidade_nova, codigo_lido)

# 3. Mandando a ordem e salvando no cofre
mensageiro.execute(ordem_somar, valores)
conexao.commit()

# 4. Verificando se deu certo
if mensageiro.rowcount > 0:
    print(f"Sucesso! Foram adicionadas {quantidade_nova} unidades ao estoque.")
else:
    print("Aviso: Essa etiqueta não existe no sistema. É preciso fazer um cadastro novo primeiro.")

# Fechando as portas
mensageiro.close()
conexao.close()