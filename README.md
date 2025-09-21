# Monorepo Template 🚀

**Template Base para Projetos Full-Stack** - Monorepo completo com API Flask e Client React

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)
[![React](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-3178c6.svg)](https://typescriptlang.org)

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação Rápida](#-instalação-rápida)
- [Setup para Novos Projetos](#-setup-para-novos-projetos)
- [Desenvolvimento](#-desenvolvimento)
- [Scripts Disponíveis](#-scripts-disponíveis)
- [API Endpoints](#-api-endpoints)
- [Estrutura Detalhada](#-estrutura-detalhada)
- [Docker](#-docker)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Contribuição](#-contribuição)
- [Troubleshooting](#-troubleshooting)

## 🎯 Visão Geral

Este **Monorepo Template** é uma base completa para projetos full-stack construída como um **monorepo** moderno. O template combina uma API robusta em Flask com um client React moderno, oferecendo uma solução full-stack pronta para ser customizada para qualquer domínio de negócio.

### ✨ Principais Funcionalidades

- 🔐 **Autenticação JWT** completa e segura
- 👥 **Gestão de Usuários** com CRUD completo
- 📊 **Dashboard** com estatísticas em tempo real
- 🎨 **Interface Moderna** com Tailwind CSS
- 📱 **Design Responsivo** para todos os dispositivos
- 🔄 **Estado Gerenciado** com React Query e Zustand
- 🐳 **Containerização** com Docker
- 🧪 **Testes Automatizados** para frontend e backend
- 📝 **Validação** ponta a ponta com Zod
- 🚀 **Performance** otimizada
- 🛠️ **Scripts Automatizados** para setup de novos projetos
- 📚 **Documentação Completa** para desenvolvedores

## 🏗️ Arquitetura

### Monorepo Structure
```
monorepo-template/
├── 📦 packages/contracts/    # Contratos compartilhados (Zod + TypeScript)
├── 🔧 api/                  # API Flask (Backend)
├── 💻 client/               # Client React (Frontend)
├── 🐳 docker-compose.yml    # Orquestração de serviços
├── 📜 Makefile             # Scripts de automação
└── 📚 docs/                # Documentação
```

### Stack Tecnológico

#### Backend (API)
- **Flask 3.0+** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados principal
- **Redis** - Cache e sessões
- **JWT** - Autenticação stateless
- **Marshmallow** - Serialização e validação
- **Celery** - Tarefas assíncronas
- **Gunicorn** - Servidor WSGI

#### Frontend (Client)
- **React 18** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS
- **React Query** - Gerenciamento de estado servidor
- **Zustand** - Estado local
- **React Router** - Roteamento
- **Axios** - Cliente HTTP

#### Compartilhado
- **Zod** - Validação de schemas
- **TypeScript** - Tipos compartilhados
- **OpenAPI** - Especificação da API

## 📁 Estrutura do Projeto

```
monorepo-template/
├── 📄 README.md                    # Este arquivo
├── 📄 DEVELOPMENT.md              # Guia de desenvolvimento
├── 📄 package.json                # Configuração do monorepo
├── 📄 Makefile                    # Scripts de automação
├── 📄 docker-compose.yml          # Orquestração Docker
├── 📄 .gitignore                  # Arquivos ignorados pelo Git
├── 📄 .editorconfig               # Configuração do editor
├── 📄 env.example                 # Variáveis de ambiente exemplo
│
├── 📦 packages/
│   └── contracts/                 # Contratos compartilhados
│       ├── 📄 package.json
│       ├── 📄 tsconfig.json
│       ├── 📄 openapi.yaml        # Especificação OpenAPI
│       └── src/
│           ├── 📄 index.ts        # Exportações principais
│           ├── 📄 auth.ts         # Schemas de autenticação
│           ├── 📄 users.ts        # Schemas de usuários
│           └── 📄 common.ts       # Tipos comuns
│
├── 🔧 api/                        # API Flask (Backend)
│   ├── 📄 pyproject.toml          # Configuração Python
│   ├── 📄 requirements.txt        # Dependências Python
│   ├── 📄 Dockerfile              # Imagem Docker
│   ├── 📄 wsgi.py                 # Entry point WSGI
│   ├── 📄 manage.py               # Scripts de gerenciamento
│   ├── 📄 env.example             # Variáveis de ambiente
│   ├── 📁 migrations/             # Migrações do banco
│   ├── 📁 instance/               # Configurações de instância
│   └── 📁 app/                    # Código da aplicação
│       ├── 📄 __init__.py         # Factory da aplicação
│       ├── 📄 config.py           # Configurações
│       ├── 📄 extensions.py       # Extensões Flask
│       ├── 📁 core/               # Utilitários centrais
│       │   ├── 📄 exceptions.py   # Exceções customizadas
│       │   ├── 📄 security.py     # Utilitários de segurança
│       │   ├── 📄 pagination.py   # Paginação
│       │   ├── 📄 logging.py      # Sistema de logs
│       │   └── 📄 utils.py        # Utilitários gerais
│       ├── 📁 domain/             # Camada de domínio
│       │   ├── 📄 models.py       # Modelos do banco
│       │   └── 📄 dtos.py         # Data Transfer Objects
│       ├── 📁 infra/              # Infraestrutura
│       │   ├── 📁 repositories/   # Repositórios
│       │   │   ├── 📄 base.py     # Repositório base
│       │   │   └── 📄 user_repo.py # Repositório de usuários
│       │   ├── 📄 mailer.py       # Sistema de email
│       │   ├── 📄 storage.py      # Armazenamento
│       │   └── 📄 tasks.py        # Tarefas assíncronas
│       ├── 📁 api/                # Camada de API
│       │   ├── 📁 health/         # Health checks
│       │   └── 📁 v1/             # API v1
│       │       ├── 📁 auth/       # Autenticação
│       │       │   ├── 📄 routes.py    # Rotas de auth
│       │       │   ├── 📄 service.py   # Lógica de auth
│       │       │   └── 📄 schemas.py   # Schemas Marshmallow
│       │       └── 📁 users/      # Usuários
│       │           ├── 📄 routes.py    # Rotas de usuários
│       │           ├── 📄 service.py   # Lógica de usuários
│       │           └── 📄 schemas.py   # Schemas de usuários
│       ├── 📁 tasks/              # Tarefas Celery
│       └── 📄 cli.py              # Comandos CLI
│
└── 💻 client/                     # Client React (Frontend)
    ├── 📄 package.json            # Dependências Node.js
    ├── 📄 tsconfig.json           # Configuração TypeScript
    ├── 📄 vite.config.ts          # Configuração Vite
    ├── 📄 tailwind.config.js      # Configuração Tailwind
    ├── 📄 postcss.config.js       # Configuração PostCSS
    ├── 📄 vitest.config.ts        # Configuração de testes
    ├── 📄 .eslintrc.cjs           # Configuração ESLint
    ├── 📄 Dockerfile              # Imagem Docker
    ├── 📄 index.html              # HTML principal
    ├── 📄 env.example             # Variáveis de ambiente
    └── 📁 src/                    # Código fonte
        ├── 📄 app/
        │   ├── 📄 main.tsx        # Entry point
        │   ├── 📄 App.tsx         # Componente principal
        │   └── 📁 store/          # Estado global
        ├── 📁 lib/                # Utilitários
        │   ├── 📄 apiClient.ts    # Cliente HTTP
        │   ├── 📄 auth.ts         # Gerenciamento de auth
        │   ├── 📄 env.ts          # Variáveis de ambiente
        │   ├── 📄 types.ts        # Tipos TypeScript
        │   └── 📄 utils.ts        # Utilitários gerais
        ├── 📁 features/           # Funcionalidades
        │   ├── 📁 auth/           # Autenticação
        │   │   ├── 📁 pages/      # Páginas de auth
        │   │   ├── 📁 components/ # Componentes de auth
        │   │   └── 📄 api.ts      # Hooks de API
        │   ├── 📁 users/          # Usuários
        │   │   ├── 📁 pages/      # Páginas de usuários
        │   │   ├── 📁 components/ # Componentes de usuários
        │   │   └── 📄 api.ts      # Hooks de API
        │   └── 📁 dashboard/      # Dashboard
        │       └── 📁 pages/      # Páginas do dashboard
        ├── 📁 components/         # Componentes reutilizáveis
        │   ├── 📄 Button.tsx      # Botão
        │   ├── 📄 Input.tsx       # Input
        │   ├── 📄 Card.tsx        # Card
        │   ├── 📄 Layout.tsx      # Layout principal
        │   └── 📄 ProtectedRoute.tsx # Rota protegida
        ├── 📁 styles/             # Estilos
        │   └── 📄 index.css       # CSS principal
        └── 📁 __tests__/          # Testes
            └── 📄 setup.ts        # Configuração de testes
```

## 🛠️ Tecnologias

### Backend (API)
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.10 | Linguagem principal |
| **Flask** | 3.0+ | Framework web |
| **SQLAlchemy** | 3.1+ | ORM |
| **PostgreSQL** | 16+ | Banco de dados |
| **Redis** | 7+ | Cache |
| **JWT** | 4.6+ | Autenticação |
| **Marshmallow** | 3.20+ | Serialização |
| **Celery** | 5.3+ | Tarefas assíncronas |
| **Gunicorn** | 21.2+ | Servidor WSGI |

### Frontend (Client)
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Node.js** | 18+ | Runtime JavaScript |
| **React** | 18+ | Biblioteca de UI |
| **TypeScript** | 5.0+ | Tipagem estática |
| **Vite** | 5.0+ | Build tool |
| **Tailwind CSS** | 3.3+ | Framework CSS |
| **React Query** | 5.17+ | Estado servidor |
| **Zustand** | 4.4+ | Estado local |
| **React Router** | 6.20+ | Roteamento |
| **Axios** | 1.6+ | Cliente HTTP |

### Compartilhado
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Zod** | 3.22+ | Validação de schemas |
| **TypeScript** | 5.0+ | Tipos compartilhados |
| **OpenAPI** | 3.0+ | Especificação da API |

## 📋 Pré-requisitos

### Obrigatórios
- **Node.js** 18.0+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://python.org/))
- **Git** ([Download](https://git-scm.com/))

### Opcionais (Recomendados)
- **Docker** 20.0+ ([Download](https://docker.com/))
- **Docker Compose** 2.0+ (incluído no Docker Desktop)
- **PostgreSQL** 16+ (se não usar Docker)
- **Redis** 7+ (se não usar Docker)

### Ferramentas de Desenvolvimento
- **VS Code** com extensões:
  - Python
  - TypeScript
  - Tailwind CSS IntelliSense
  - ESLint
  - Prettier
- **Postman** ou **Insomnia** (para testar API)

## 🚀 Instalação Rápida

### 1. Clone o Template
```bash
git clone <repository-url>
cd monorepo-template
```

### 2. Instale Dependências
```bash
# Instala todas as dependências
make setup

# Ou manualmente:
npm install
cd packages/contracts && npm install
cd ../../client && npm install
cd ../api && pip install -e .
```

### 3. Configure Variáveis de Ambiente
```bash
# Copie os arquivos de exemplo
cp env.example .env
cp api/env.example api/.env
cp client/env.example client/.env

# Edite os arquivos conforme necessário
```

### 4. Inicie os Serviços

#### Opção A: Com Docker (Recomendado)
```bash
make docker-up
```

#### Opção B: Desenvolvimento Local
```bash
# Terminal 1: API
make dev-api

# Terminal 2: Client
make dev-client
```

### 5. Acesse a Aplicação
- **Client**: http://localhost:5173
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health

## 🆕 Setup para Novos Projetos

### Opção 1: Script Automático (Recomendado)

#### Linux/macOS
```bash
./setup-new-project.sh "meu-projeto" "MeuApp"
```

#### Windows PowerShell
```powershell
.\setup-new-project.ps1 -ProjectName "meu-projeto" -AppName "MeuApp"
```

### Opção 2: Manual

#### 1. Personalize o Projeto
```bash
# Renomeie o projeto
find . -type f -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" | xargs sed -i 's/monorepo-template/SEU-PROJETO/g'
find . -type f -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" | xargs sed -i 's/MonorepoApp/SEU-APP/g'

# Atualize as variáveis de ambiente
# Edite .env, api/.env, client/.env com suas configurações
```

### 2. Configure o Banco de Dados
```bash
# Atualize o nome do banco em:
# - .env
# - api/.env
# - docker-compose.yml

# Execute as migrações
cd api
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Personalize os Modelos
```bash
# Edite api/app/domain/models.py
# Adicione seus modelos específicos do domínio
# Remova os modelos de exemplo (User, Job)
```

### 4. Configure as Rotas
```bash
# Edite api/app/api/v1/
# Adicione suas rotas específicas
# Remova as rotas de exemplo
```

### 5. Personalize o Frontend
```bash
# Edite client/src/features/
# Adicione suas funcionalidades específicas
# Remova as features de exemplo
```

### 6. Atualize a Documentação
```bash
# Edite README.md
# Atualize com informações do seu projeto
# Remova referências genéricas
```

## 💻 Desenvolvimento

### Comandos Principais

```bash
# Desenvolvimento completo
make dev

# Serviços individuais
make dev-api      # Apenas API
make dev-client   # Apenas Client

# Build
make build

# Testes
make test

# Linting
make lint

# Docker
make docker-up    # Iniciar serviços
make docker-down  # Parar serviços
make docker-logs  # Ver logs

# Limpeza
make clean
```

### URLs de Desenvolvimento

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Client** | http://localhost:5173 | Interface do usuário |
| **API** | http://localhost:8000 | API REST |
| **Health** | http://localhost:8000/api/health | Status dos serviços |
| **API Docs** | http://localhost:8000/api/docs | Documentação da API |

## 📜 Scripts Disponíveis

### Desenvolvimento
```bash
make dev              # Inicia todos os serviços
make dev-api          # Inicia apenas a API
make dev-client       # Inicia apenas o Client
```

### Build
```bash
make build            # Build de todos os projetos
make build-contracts  # Build dos contratos
make build-client     # Build do Client
```

### Testes
```bash
make test             # Executa todos os testes
make test-client      # Testes do Client
```

### Linting
```bash
make lint             # Executa todos os linters
make lint-client      # Linter do Client
```

### Docker
```bash
make docker-up        # Inicia serviços com Docker
make docker-down      # Para serviços
make docker-logs      # Mostra logs
make docker-build     # Build das imagens
```

### Limpeza
```bash
make clean            # Limpa todos os builds
make clean-client     # Limpa build do Client
make clean-api        # Limpa build da API
```

## 🔌 API Endpoints

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/auth/login` | Login do usuário |
| `POST` | `/api/v1/auth/register` | Registro de usuário |
| `POST` | `/api/v1/auth/logout` | Logout do usuário |
| `POST` | `/api/v1/auth/refresh` | Renovar token |
| `GET` | `/api/v1/auth/me` | Dados do usuário atual |
| `POST` | `/api/v1/auth/change-password` | Alterar senha |

### Usuários
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/users` | Listar usuários |
| `POST` | `/api/v1/users` | Criar usuário |
| `GET` | `/api/v1/users/{id}` | Obter usuário |
| `PUT` | `/api/v1/users/{id}` | Atualizar usuário |
| `DELETE` | `/api/v1/users/{id}` | Excluir usuário |
| `POST` | `/api/v1/users/{id}/activate` | Ativar usuário |
| `POST` | `/api/v1/users/{id}/deactivate` | Desativar usuário |
| `GET` | `/api/v1/users/stats` | Estatísticas de usuários |

### Health Check
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/health` | Status geral |
| `GET` | `/api/health/ready` | Pronto para receber tráfego |
| `GET` | `/api/health/live` | Aplicação viva |

### Exemplo de Uso da API

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'

# Listar usuários (com autenticação)
curl -X GET http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer <token>"

# Health check
curl -X GET http://localhost:8000/api/health
```

## 🏗️ Estrutura Detalhada

### API (Backend)

#### Arquitetura Limpa
A API segue os princípios da **Clean Architecture** com separação clara de responsabilidades:

- **Core**: Utilitários centrais (exceptions, security, pagination)
- **Domain**: Modelos de negócio e DTOs
- **Infra**: Repositórios e infraestrutura
- **API**: Controllers e rotas

#### Modelos de Dados
```python
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Autenticação JWT
- **Access Token**: 1 hora de duração
- **Refresh Token**: 30 dias de duração
- **Blacklist**: Revogação de tokens
- **Headers**: `Authorization: Bearer <token>`

#### Validação
- **Marshmallow**: Serialização e validação
- **Zod**: Validação compartilhada com frontend
- **Sanitização**: Limpeza de dados de entrada

### Client (Frontend)

#### Arquitetura Moderna
O Client utiliza uma arquitetura moderna com separação de responsabilidades:

- **Features**: Funcionalidades organizadas por domínio
- **Components**: Componentes reutilizáveis
- **Lib**: Utilitários e configurações
- **App**: Configuração principal

#### Gerenciamento de Estado
- **React Query**: Estado do servidor (cache, sincronização)
- **Zustand**: Estado local (autenticação, UI)
- **Context**: Estado compartilhado entre componentes

#### Design System
Componentes reutilizáveis com Tailwind CSS:
- **Button**: Botões com variantes e estados
- **Input**: Campos de entrada com validação
- **Card**: Containers de conteúdo
- **Layout**: Layout principal da aplicação

### Contratos Compartilhados

#### Validação Ponta a Ponta
```typescript
// Schema Zod compartilhado
export const LoginRequest = z.object({
  email: z.string().email("Email inválido"),
  password: z.string().min(6, "Senha deve ter pelo menos 6 caracteres"),
});

// Uso no frontend
const { data, error } = useLogin(loginData);

// Uso no backend
@auth_bp.route('/login', methods=['POST'])
def login():
    data = login_schema.load(request.json)
    # ...
```

## 🐳 Docker

### Serviços Incluídos
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e sessões
- **API**: Aplicação Flask
- **Client**: Aplicação React

### Comandos Docker
```bash
# Iniciar todos os serviços
make docker-up

# Parar serviços
make docker-down

# Ver logs
make docker-logs

# Build das imagens
make docker-build

# Logs de um serviço específico
docker-compose logs -f api
docker-compose logs -f client
```

### Configuração Docker
```yaml
# docker-compose.yml
version: '3.9'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: vagafacil
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  
  client:
    build: ./client
    ports:
      - "5173:5173"
    depends_on:
      - api
```

## 🧪 Testes

### Frontend (Client)
```bash
# Executar testes
make test-client

# Testes com interface visual
cd client && npm run test:ui

# Testes com cobertura
cd client && npm run test:coverage
```

**Tecnologias de Teste:**
- **Vitest**: Runner de testes
- **React Testing Library**: Testes de componentes
- **Jest DOM**: Matchers customizados
- **MSW**: Mock Service Worker para API

### Backend (API)
```bash
# Executar testes
cd api && pytest

# Testes com cobertura
cd api && pytest --cov

# Testes específicos
cd api && pytest tests/test_auth.py
```

**Tecnologias de Teste:**
- **pytest**: Framework de testes
- **pytest-flask**: Extensões para Flask
- **factory-boy**: Factories para dados de teste
- **faker**: Geração de dados fake

### Exemplo de Teste
```typescript
// client/src/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react'
import { Button } from '@/components/Button'

test('renders button with text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})
```

```python
# api/tests/test_auth.py
def test_login_success(client, user):
    response = client.post('/api/v1/auth/login', json={
        'email': user.email,
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
```

## 🚀 Deploy

### Desenvolvimento
```bash
# Com Docker (recomendado)
make docker-up
```

### Produção
```bash
# Build das imagens
make docker-build

# Deploy com docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Variáveis de Ambiente de Produção
```bash
# .env.prod
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/vagafacil
REDIS_URL=redis://host:6379/0
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=https://your-domain.com
```

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Clone** seu fork: `git clone <your-fork>`
3. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
4. **Faça** suas alterações
5. **Execute** os testes: `make test`
6. **Execute** o linter: `make lint`
7. **Commit** suas alterações: `git commit -m "feat: adiciona nova funcionalidade"`
8. **Push** para sua branch: `git push origin feature/nova-funcionalidade`
9. **Abra** um Pull Request

### Padrões de Commit
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: formatação de código
refactor: refatoração
test: adiciona testes
chore: tarefas de manutenção
```

### Checklist de Pull Request
- [ ] Código testado localmente
- [ ] Testes passando (`make test`)
- [ ] Linter passando (`make lint`)
- [ ] Documentação atualizada
- [ ] Commits seguem o padrão
- [ ] Branch atualizada com main

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Verificar logs do banco
docker-compose logs db

# Reiniciar serviços
make docker-down && make docker-up
```

#### 2. Erro de CORS
```bash
# Verificar FRONTEND_URL no .env da API
echo $FRONTEND_URL

# Deve ser: http://localhost:5173
```

#### 3. Erro de Dependências
```bash
# Limpar e reinstalar
make clean
make setup
```

#### 4. Problemas com Docker
```bash
# Limpar containers e volumes
docker-compose down -v
docker system prune -f
make docker-up
```

#### 5. Erro de Porta em Uso
```bash
# Verificar portas em uso
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173

# Parar processos
sudo kill -9 <PID>
```

### Logs e Debugging

#### Ver Logs
```bash
# Todos os serviços
make docker-logs

# Serviço específico
docker-compose logs -f api
docker-compose logs -f client

# Logs da API
cd api && flask logs
```

#### Debug Mode
```bash
# API em modo debug
cd api
export FLASK_DEBUG=true
flask run

# Client em modo debug
cd client
npm run dev
```

### Performance

#### Otimizações da API
- **Connection Pooling**: SQLAlchemy com pool de conexões
- **Redis Cache**: Cache de consultas frequentes
- **Gunicorn**: Múltiplos workers
- **Compression**: Gzip habilitado

#### Otimizações do Client
- **Code Splitting**: Lazy loading de rotas
- **Tree Shaking**: Remoção de código não usado
- **Image Optimization**: Otimização de imagens
- **Bundle Analysis**: Análise do bundle

## 📚 Documentação Adicional

- [Guia de Desenvolvimento](DEVELOPMENT.md) - Guia detalhado para desenvolvedores
- [API Documentation](http://localhost:8000/api/docs) - Documentação interativa da API
- [OpenAPI Spec](packages/contracts/openapi.yaml) - Especificação OpenAPI

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Flask** - Framework web Python
- **React** - Biblioteca de interface
- **Tailwind CSS** - Framework CSS
- **Vite** - Build tool moderno
- **Docker** - Containerização
- **PostgreSQL** - Banco de dados
- **Redis** - Cache

---

**Monorepo Template** - Base para Projetos Full-Stack 🚀

Desenvolvido com ❤️ usando tecnologias modernas e melhores práticas de desenvolvimento.

## 📚 Documentação Adicional

- [Guia do Template](TEMPLATE_GUIDE.md) - Guia específico para usar o template
- [Guia de Desenvolvimento](DEVELOPMENT.md) - Guia detalhado para desenvolvedores
- [API Documentation](http://localhost:8000/api/docs) - Documentação interativa da API
- [OpenAPI Spec](packages/contracts/openapi.yaml) - Especificação OpenAPI

## 🚀 Como Usar Este Template

1. **Clone** o template
2. **Execute** o script de setup
3. **Personalize** para seu projeto
4. **Desenvolva** suas funcionalidades
5. **Deploy** em produção

Para mais detalhes, consulte o [Guia do Template](TEMPLATE_GUIDE.md).