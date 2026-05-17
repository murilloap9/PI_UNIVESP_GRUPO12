CREATE DATABASE estoque_hospitalar;
USE estoque_hospitalar;

CREATE TABLE acessorios (
    codigo_qr VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100),
    quantidade INT
);
SELECT * FROM acessorios