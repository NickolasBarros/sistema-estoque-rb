# Mercearia Horizonte — Gestão de Estoque

Projeto acadêmico de Estrutura de Dados: um sistema de controle de estoque para uma mercearia de bairro fictícia. O cenário dá propósito às operações: a equipe cadastra produtos, recebe reposições, registra saídas do balcão e acompanha itens que chegaram ao estoque mínimo.

**Faculdade Anhanguera Turu — Projeto de Estrutura de Dados**

**Alunos:** Kelvem Mendonça Nazaré, Karin Shamir Tawill Tamarony, Nickolas Gabriel Barros Dutra e Victor Trajanno Agame de Souza.

## O que o sistema demonstra

- Cadastro de produtos com SKU, categoria, unidade e limite mínimo.
- Consulta e listagem de produtos ordenados por SKU.
- Registro de entradas e saídas com histórico e data/hora.
- Painel com total de produtos, unidades disponíveis e alertas de reposição.
- Árvore Rubro-Negra implementada no projeto para indexar produtos por SKU, mantendo busca, inclusão e remoção em **O(log n)**.
- Validação das propriedades da árvore pelo endpoint `/api/arvore/validar`.
- Catálogo fictício carregado ao iniciar a API para permitir uma demonstração imediata.

## Organização orientada a objetos

- `models/produto.py`: classe `Produto` representa os dados e o comportamento de serialização de um produto.
- `models/movimentacao.py`: classe `Movimentacao` representa uma entrada ou saída.
- `services/estoque_service.py`: classe `EstoqueService` coordena as regras de negócio e usa a árvore para armazenar/buscar produtos.
- `data_structures/arvore_rb.py`: classes `No` e `ArvoreRB` implementam os nós, cores, rotações, busca e balanceamento.
- `api/routes.py`: recebe requisições HTTP e encaminha as operações ao serviço.
- `frontend/src/App.jsx`: interface React que consome a API.

Essa separação ajuda a explicar o fluxo na apresentação: a tela envia uma requisição, a rota chama o serviço, o serviço aplica a regra de negócio e a árvore mantém os produtos organizados.

## Como executar

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

A API ficará disponível em `http://localhost:5000/api`.

### Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Abra o endereço apresentado pelo Vite, normalmente `http://localhost:5173`.

### Testes

```bash
cd backend
pytest tests -v
```

## Roteiro para demonstrar

1. Abra o painel da Mercearia Horizonte e apresente os indicadores e alertas de reposição.
2. Cadastre um produto, como café ou leite, definindo quantidade e estoque mínimo.
3. Use a busca por SKU e registre uma saída para demonstrar a atualização do saldo e do histórico.
4. Explique que o SKU é a chave da árvore e que as rotações preservam o balanceamento após inclusões e remoções.
5. Consulte `http://localhost:5000/api/arvore/validar` para mostrar a validação da estrutura.

## Escopo acadêmico

Os dados ficam em memória e são reiniciados quando o backend para; a API carrega produtos fictícios ao iniciar para facilitar a demonstração. O PostgreSQL e `database/schema.sql` representam uma possibilidade de persistência futura, mas ainda não estão conectados à aplicação. Portanto, este protótipo demonstra as operações e a estrutura de dados, não substituindo um sistema comercial de produção.
