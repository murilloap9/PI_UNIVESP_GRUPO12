import mysql.connector

# Abrindo o cofre
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="estoque_hospitalar"
)

mensageiro = conexao.cursor()

# A ordem para guardar os itens
ordem = "INSERT INTO acessorios (codigo_qr, nome, quantidade) VALUES (%s, %s, %s)"

# A nossa lista com todos os equipamentos
lista_de_equipamentos = [
    ("QR-002", "Manguito", 15),
    ("QR-003", "Cabo de Manguito", 10),
    ("QR-004", "Sensor de Oximetria", 20)
]

# Mandando o mensageiro entregar a lista inteira de uma vez!
# Repare na palavra "executemany" abaixo:
mensageiro.executemany(ordem, lista_de_equipamentos)
conexao.commit() # Isso é o que salva as informações de verdade

print("Todos os equipamentos foram guardados no estoque com sucesso!")

# Fechando as portas
mensageiro.close()
conexao.close()