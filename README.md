# Sistema de Gestão de Estoque com Árvore Rubro-Negra

Projeto de Estrutura de Dados — Faculdade Anhanguera Turu

**Alunos:**
- Kelvem Mendonça Nazaré
- Karin Shamir Tawill Tamarony
- Nickolas Gabriel Barros Dutra
- Victor Trajanno Agame de Souza

## Como rodar

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Testes

```bash
cd backend
pytest tests -v
```

## Tecnologias

- Python + Flask (backend)
- Árvore Rubro-Negra (estrutura de dados)
- React + Vite (frontend)
- PostgreSQL (banco de dados)