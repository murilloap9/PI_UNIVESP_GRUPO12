import mysql.connector

# Abrindo o nosso cofre
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="estoque_hospitalar"
)

mensageiro = conexao.cursor()

# 1. A tela espera a maquininha dar o "bipe" (ou você digitar)
codigo_lido = input("Passe o leitor na etiqueta (ou digite o código): ")

# 2. A regra de subtração: diminui 1 da quantidade, desde que ainda tenha no estoque
ordem_diminuir = "UPDATE acessorios SET quantidade = quantidade - 1 WHERE codigo_qr = %s AND quantidade > 0"

# Atenção aqui: como é só um código agora, essa vírgula no final é obrigatória 
# para não dar aquele mesmo erro da embalagem que tivemos antes!
valores = (codigo_lido,) 

# 3. Mandando a ordem e salvando no cofre
mensageiro.execute(ordem_diminuir, valores)
conexao.commit()

# 4. Avisando se deu certo
if mensageiro.rowcount > 0:
    print("Sucesso! O estoque foi atualizado.")
else:
    print("Aviso: Peça não encontrada ou o estoque já está no zero!")

# Fechando as portas
mensageiro.close()
conexao.close()