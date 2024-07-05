## Install

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py --debug run --host=0.0.0.0 --port=8080 // Roda o servidor run em tempo real

## Git

git add . // Adiciona todos os arquivos

git commit -m "Mensagem" // Commita os arquivos

git push // Envia para o repositório

### Entidades

- Produtos
	- Nome
	- Preço
	- Categoria => Bebida, Comida, etc.
		- Criar ENUM
	- Estoque
	- Imagem => Cloudinary url
- Garçons
	- Nome
	- Email
	- Telefone
	- Senha
	- Ativo => Boolean
- Mesas
	- Numero
	- Ativa => Boolean
	- Em uso => Boolean
	- Garçom
		- Nome
		- Id
- Pedidos
	- Garçom
		- ID
	- Mesa
		- Numero
		- ID
	- Produtos => Array com
		- Produto
			- ID
			- Nome
			- Valor
		- Quantidade
	- Total => soma de todos
	- Forma de pagamento => Pix, Cartao ou dinheiro
		- Criar ENUM
	- Status => Aguardando, Pago, Entregue
		- Criar ENUM
	- Criado em => Data
	- Atualizado em => Data
	- Finalizado em => Data



### Endpoints

Ex.: Produtos = 
	GET /produtos
	PUT /produtos/produtoID

- Produtos
	1 Listar produtos
		- Filtros
			- Categoria
			- Nome
			- Ordem crescente e decrescente por nome
			- Ordem crescente e decrescente por qnt em estoque
	2 Criar produto
	3 Editar produto
	4 Remover produto
- Garçons
	1 Listar garçons
		- Filtros
			- Categoria
			- Ordem crescente e decrescente por nome
	2 Criar garçom
	3 Editar garçom
	4 Remover garçom
- Mesas
	1 Listar mesas
		- Filtros
			- Em uso => booleano
			- Categoria
			- Ordem crescente e decrescente por numero
	2 Criar mesa
	3 Editar mesa
	4 Remover mesa
- Pedidos 
	1 Listar pedidos em andamento
		- Filtros
			- Busca por garçom
			- Ordem cresc. descr. por numero de mesa
			- Status do pedido
	2 Criar pedido
	3 Atualizar pedido
	4 Cancelar pedido
- Autenticação
	1 Login
		- JWT

- Websocket
	1 Enviar pedido para Dashboard
	2 Marcar mesa em uso

- Relatório
	1 Simplificado => Versão garçom
		- Qunt. pedidos
		- Total Valor
		- Faturamento (10%)

	2 Completo
		- Atendimento
			- garçons em serviço
			- Mesas
			- Qntd. Pedidos
		- Geral
			- Valor em dinheiro
		- Vendas
			- Qntd. pedidos
			- Pedidos balcão
			- Valor total de pedidos
			- Valor bruto
		- Faturamento
			- Garçons
			- Maquininha
			- Balcao
			- Total faturamento
	3 Garcons
		Filtros
			Ordem crescente e descrescente pelo vlaor total
			Buscar por nome de garçom
		Array Garçons
			 - nome
			 - pedidos
			 - total