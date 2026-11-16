# HelpDesk AI — Sistema Inteligente de Help Desk

Sistema web de gerenciamento de chamados de suporte técnico, desenvolvido para organizar solicitações, acompanhar atendimentos e facilitar a comunicação entre usuários e equipe de TI.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento, organização de código, autenticação, controle de acesso e integração entre frontend, backend e banco de dados.

## Funcionalidades

- Cadastro e autenticação de usuários.
- Login com autenticação baseada em token JWT.
- Controle de acesso por perfil:
  - EMPLOYEE — abertura e acompanhamento de chamados.
  - TECHNICIAN — atendimento e atualização de chamados.
  - ADMIN — perfil administrativo.
- Abertura e listagem de chamados.
- Atualização de status dos chamados.
- Classificação por categoria e prioridade.
- Comentários nos chamados.
- Dashboard com indicadores de atendimento.
- Classificação automática de chamados baseada em palavras-chave.

## Tecnologias utilizadas

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT

### Frontend
- React
- TypeScript
- Tailwind CSS

### Infraestrutura e ferramentas
- Docker
- Docker Compose
- Git e GitHub
- Swagger / OpenAPI

## Arquitetura do projeto

```text
HelpDesk-AI/
├── backend/
│   └── app/
├── frontend/
├── database/
├── docs/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Como executar o projeto

### Pré-requisitos

- Docker Desktop instalado.
- Git instalado.
- Visual Studio Code (opcional).

### 1. Clonar o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd HelpDesk-AI
```

### 2. Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

No PowerShell:

```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e configure os valores necessários, incluindo uma chave secreta própria e uma senha para o PostgreSQL.

Não compartilhe nem publique o arquivo `.env`.

### 3. Iniciar a aplicação

Na pasta principal do projeto, execute:

```bash
docker compose up -d --build
```

### 4. Acessar o sistema

- Frontend: http://localhost:5173
- Documentação da API: http://localhost:8000/docs
- API: http://localhost:8000

## Testes da API

A API pode ser explorada pela documentação interativa Swagger.

Principais operações:

- Cadastro e login.
- Consulta do usuário autenticado.
- Criação e consulta de chamados.
- Atualização de chamados.
- Inclusão e consulta de comentários.
- Consulta dos indicadores do dashboard.
- Classificação automática de chamados.

## Segurança

- Senhas armazenadas com hash.
- Autenticação baseada em JWT.
- Rotas protegidas.
- Controle de permissões por perfil.
- Variáveis sensíveis mantidas em arquivo `.env`.
- Arquivo `.env` excluído do versionamento.

## Objetivo do projeto

Este projeto tem como objetivo aplicar conhecimentos de desenvolvimento Full Stack, construção de APIs REST, integração com banco de dados relacionais, autenticação, containers e desenvolvimento de interfaces web.

Também representa parte da minha evolução acadêmica e profissional na área de Análise e Desenvolvimento de Sistemas.

## Autora

Desenvolvido como projeto de portfólio para demonstrar conhecimentos em desenvolvimento de software, backend, frontend e banco de dados.