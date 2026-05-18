
MANUAL DE EXECUÇÃO - CONTROLE DE ESTOQUE ENGENHARIA CLÍNICA

Este guia prático mostra como ligar e rodar o sistema de controle 
de estoque hospitalar no seu computador passo a passo.

-------------------------------------------------------------------
O QUE VOCÊ PRECISA TER INSTALADO:
-------------------------------------------------------------------
1. Python (para rodar o servidor e a tela)
2. MySQL Workbench (onde ficam guardadas as informações do estoque)

-------------------------------------------------------------------
PASSO 1: PREPARAR O BANCO DE DADOS (SÓ PRECISA FAZER UMA VEZ)
-------------------------------------------------------------------
1. Abra o seu MySQL Workbench e conecte-se com seu usuário e senha.
2. Clique no ícone de uma folha de papel com um raio azul (Nova Guia de Consulta).
3. Copie e cole o código abaixo dentro dessa guia:

   CREATE DATABASE estoque_hospitalar;
   USE estoque_hospitalar;
   CREATE TABLE acessorios (
       id INT AUTO_INCREMENT PRIMARY KEY,
       codigo_qr VARCHAR(100) NOT NULL,
       nome VARCHAR(255) NOT NULL,
       quantidade INT DEFAULT 0
   );

4. Clique no botão do raio azul sozinho para rodar os comandos. 
   Uma bolinha verde com um check (de sucesso) deve aparecer embaixo.

-------------------------------------------------------------------
PASSO 2: LIGAR O BACK-END
-------------------------------------------------------------------
1. Abra o seu editor de código ou o terminal do Windows.
2. Navegue até a pasta onde está o arquivo 'servidor.py' usando o comando:
   cd caminho/da/sua/pasta/back
3. Abra o arquivo 'servidor.py' e confira se a sua senha do banco de dados 
   está certinha. Salve o arquivo.
4. No terminal, digite o seguinte comando para ligar o motor:
   python servidor.py
5. Mantenha essa janela aberta. O motor precisa ficar ligado o tempo todo.

-------------------------------------------------------------------
PASSO 3: LIGAR O FRONT-END
-------------------------------------------------------------------
1. Abra um NOVO terminal.
2. Navegue até a pasta onde está a sua tela 'index.html' usando o comando:
   cd caminho/da/sua/pasta/front
3. Digite o comando abaixo para fazer a tela funcionar como um site real:
   python -m http.server 8000
4. Mantenha essa segunda janela aberta também.

-------------------------------------------------------------------
PASSO 4: USAR O SISTEMA NO NAVEGADOR
-------------------------------------------------------------------
1. Abra o seu navegador de internet (de sua preferência).
2. Na barra de endereços lá em cima, digite exatamente isto e dê Enter:
   http://localhost:8000
3. Pronto! O sistema vai abrir limpinho e totalmente integrado com o leitor 
   de código QR e com o banco de dados.

-------------------------------------------------------------------
PARA FECHAR O PROGRAMA:
-------------------------------------------------------------------
Quando terminar de usar, basta ir nos dois terminais pretos e apertar 
as teclas 'Ctrl + C' no teclado. Isso desliga os servidores com segurança.
===================================================================
