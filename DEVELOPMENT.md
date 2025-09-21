# Guia de Desenvolvimento 🛠️

Este guia fornece instruções detalhadas para desenvolvedores que trabalham com o Monorepo Template.

## 📋 Índice

- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [API (Backend)](#-api-backend)
- [Client (Frontend)](#-client-frontend)
- [Testes](#-testes)
- [Docker](#-docker)
- [Deploy](#-deploy)
- [Troubleshooting](#-troubleshooting)

## 🚀 Configuração do Ambiente

### Pré-requisitos

- **Node.js** 18.0+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://python.org/))
- **Git** ([Download](https://git-scm.com/))
- **Docker** 20.0+ (opcional, mas recomendado)

### Instalação

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd monorepo-template
   ```

2. **Instale as dependências**
   ```bash
   make setup
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp env.example .env
   cp api/env.example api/.env
   cp client/env.example client/.env
   ```

4. **Configure o banco de dados**
   ```bash
   cd api
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Crie um usuário administrador**
   ```bash
   cd api
   flask create-admin
   ```

## 🏗️ Estrutura do Projeto

```
monorepo-template/
├── 📦 packages/contracts/    # Contratos compartilhados
├── 🔧 api/                  # API Flask (Backend)
├── 💻 client/               # Client React (Frontend)
├── 🐳 docker-compose.yml    # Orquestração Docker
├── 📜 Makefile             # Scripts de automação
└── 📚 docs/                # Documentação
```

### Packages/Contracts

Contém schemas Zod e tipos TypeScript compartilhados entre frontend e backend.

**Estrutura:**
- `src/common.ts` - Tipos e utilitários comuns
- `src/auth.ts` - Schemas de autenticação
- `src/users.ts` - Schemas de usuários
- `src/index.ts` - Exportações principais

### API (Backend)

Seguindo Clean Architecture com Flask.

**Estrutura:**
- `app/core/` - Utilitários centrais
- `app/domain/` - Modelos e DTOs
- `app/infra/` - Repositórios e infraestrutura
- `app/api/` - Controllers e rotas

### Client (Frontend)

React com TypeScript e Vite.

**Estrutura:**
- `src/app/` - Configuração principal
- `src/lib/` - Utilitários e configurações
- `src/features/` - Funcionalidades organizadas
- `src/components/` - Componentes reutilizáveis

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
```

### URLs de Desenvolvimento

- **Client**: http://localhost:5173
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health
- **API Docs**: http://localhost:8000/api/docs

## 🔧 API (Backend)

### Tecnologias

- **Flask** 3.0+ - Framework web
- **SQLAlchemy** 3.1+ - ORM
- **PostgreSQL** 16+ - Banco de dados
- **Redis** 7+ - Cache
- **JWT** 4.6+ - Autenticação
- **Marshmallow** 3.20+ - Serialização

### Estrutura da API

#### Core
- `exceptions.py` - Exceções customizadas
- `security.py` - Utilitários de segurança
- `pagination.py` - Paginação
- `logging.py` - Sistema de logs
- `utils.py` - Utilitários gerais

#### Domain
- `models.py` - Modelos do banco de dados
- `dtos.py` - Data Transfer Objects

#### Infra
- `repositories/` - Repositórios
- `mailer.py` - Sistema de email
- `storage.py` - Armazenamento de arquivos
- `tasks.py` - Tarefas assíncronas

#### API
- `health/` - Health checks
- `v1/auth/` - Autenticação
- `v1/users/` - Usuários

### Endpoints Disponíveis

#### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/refresh` - Renovar token
- `GET /api/v1/auth/me` - Dados do usuário atual
- `POST /api/v1/auth/change-password` - Alterar senha

#### Usuários
- `GET /api/v1/users` - Listar usuários
- `POST /api/v1/users` - Criar usuário
- `GET /api/v1/users/{id}` - Obter usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Excluir usuário
- `POST /api/v1/users/{id}/activate` - Ativar usuário
- `POST /api/v1/users/{id}/deactivate` - Desativar usuário
- `GET /api/v1/users/stats` - Estatísticas de usuários

### Desenvolvimento da API

1. **Criar novo modelo**
   ```python
   # app/domain/models.py
   class NewModel(BaseModel):
       name = db.Column(db.String(255), nullable=False)
       # ... outros campos
   ```

2. **Criar repositório**
   ```python
   # app/infra/repositories/new_model_repo.py
   class NewModelRepository(BaseRepository[NewModel]):
       def __init__(self):
           super().__init__(NewModel)
   ```

3. **Criar serviço**
   ```python
   # app/api/v1/new_model/service.py
   class NewModelService:
       def __init__(self):
           self.repo = NewModelRepository()
   ```

4. **Criar rotas**
   ```python
   # app/api/v1/new_model/routes.py
   @new_model_bp.route('/', methods=['GET'])
   @jwt_required()
   def get_new_models():
       # Implementação
   ```

5. **Registrar blueprint**
   ```python
   # app/__init__.py
   from app.api.v1.new_model import new_model_bp
   app.register_blueprint(new_model_bp, url_prefix='/api/v1/new-model')
   ```

## 💻 Client (Frontend)

### Tecnologias

- **React** 18+ - Biblioteca de UI
- **TypeScript** 5.0+ - Tipagem estática
- **Vite** 5.0+ - Build tool
- **Tailwind CSS** 3.3+ - Framework CSS
- **React Query** 5.17+ - Estado servidor
- **Zustand** 4.4+ - Estado local
- **React Router** 6.20+ - Roteamento

### Estrutura do Client

#### App
- `main.tsx` - Entry point
- `App.tsx` - Componente principal

#### Lib
- `apiClient.ts` - Cliente HTTP
- `auth.ts` - Gerenciamento de autenticação
- `env.ts` - Variáveis de ambiente
- `types.ts` - Tipos TypeScript
- `utils.ts` - Utilitários

#### Features
- `auth/` - Autenticação
- `users/` - Usuários
- `dashboard/` - Dashboard

#### Components
- `Button.tsx` - Botão
- `Input.tsx` - Input
- `Card.tsx` - Card
- `Layout.tsx` - Layout principal
- `ProtectedRoute.tsx` - Rota protegida

### Desenvolvimento do Client

1. **Criar nova feature**
   ```bash
   mkdir src/features/new-feature
   mkdir src/features/new-feature/pages
   mkdir src/features/new-feature/components
   ```

2. **Criar página**
   ```typescript
   // src/features/new-feature/pages/NewFeaturePage.tsx
   export const NewFeaturePage: React.FC = () => {
     return <div>Nova Feature</div>
   }
   ```

3. **Adicionar rota**
   ```typescript
   // src/app/App.tsx
   import { NewFeaturePage } from '@/features/new-feature/pages/NewFeaturePage'
   
   // Adicionar rota no JSX
   <Route path="/new-feature" element={<NewFeaturePage />} />
   ```

4. **Criar componente**
   ```typescript
   // src/features/new-feature/components/NewFeatureComponent.tsx
   export const NewFeatureComponent: React.FC = () => {
     return <div>Componente</div>
   }
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

**Tecnologias:**
- **Vitest** - Runner de testes
- **React Testing Library** - Testes de componentes
- **Jest DOM** - Matchers customizados

### Backend (API)

```bash
# Executar testes
cd api && pytest

# Testes com cobertura
cd api && pytest --cov

# Testes específicos
cd api && pytest tests/test_auth.py
```

**Tecnologias:**
- **pytest** - Framework de testes
- **pytest-flask** - Extensões para Flask
- **factory-boy** - Factories para dados de teste

### Exemplo de Teste Frontend

```typescript
// src/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react'
import { Button } from '@/components/Button'

test('renders button with text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})
```

### Exemplo de Teste Backend

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

## 🐳 Docker

### Desenvolvimento

```bash
# Iniciar todos os serviços
make docker-up

# Parar serviços
make docker-down

# Ver logs
make docker-logs

# Build das imagens
make docker-build
```

### Serviços Incluídos

- **PostgreSQL** - Banco de dados
- **Redis** - Cache
- **API** - Aplicação Flask
- **Client** - Aplicação React

### Configuração Docker

```yaml
# docker-compose.yml
version: '3.9'
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: monorepo_template
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

## 🚀 Deploy

### Desenvolvimento

```bash
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
DATABASE_URL=postgresql://user:pass@host:5432/database
REDIS_URL=redis://host:6379/0
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=https://your-domain.com
```

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
- **Connection Pooling** - SQLAlchemy com pool de conexões
- **Redis Cache** - Cache de consultas frequentes
- **Gunicorn** - Múltiplos workers
- **Compression** - Gzip habilitado

#### Otimizações do Client
- **Code Splitting** - Lazy loading de rotas
- **Tree Shaking** - Remoção de código não usado
- **Image Optimization** - Otimização de imagens
- **Bundle Analysis** - Análise do bundle

## 📚 Recursos Adicionais

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Vite Documentation](https://vitejs.dev/guide/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações
4. Execute os testes: `make test`
5. Execute o linter: `make lint`
6. Commit suas alterações: `git commit -m "feat: adiciona nova funcionalidade"`
7. Push para sua branch: `git push origin feature/nova-funcionalidade`
8. Abra um Pull Request

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

---

**Monorepo Template** - Guia de Desenvolvimento 🛠️

Para mais informações, consulte o [README.md](README.md) principal.
