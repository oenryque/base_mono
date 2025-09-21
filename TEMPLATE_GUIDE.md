# Guia do Template 🚀

Este guia explica como usar o Monorepo Template para criar novos projetos rapidamente.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Setup Rápido](#-setup-rápido)
- [Personalização](#-personalização)
- [Desenvolvimento](#-desenvolvimento)
- [Deploy](#-deploy)
- [Exemplos](#-exemplos)

## 🎯 Visão Geral

O Monorepo Template é uma base completa para projetos full-stack que inclui:

- ✅ **API Flask** com Clean Architecture
- ✅ **Client React** com TypeScript
- ✅ **Autenticação JWT** para devs/admins
- ✅ **Docker** para desenvolvimento e produção
- ✅ **Testes** configurados
- ✅ **Scripts de automação**
- ✅ **Documentação completa**

## 🚀 Setup Rápido

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

1. **Clone o template**
   ```bash
   git clone <template-url> meu-projeto
   cd meu-projeto
   ```

2. **Renomeie o projeto**
   ```bash
   # Substitua "monorepo-template" por "meu-projeto"
   find . -type f -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" | xargs sed -i 's/monorepo-template/meu-projeto/g'
   
   # Substitua "MonorepoApp" por "MeuApp"
   find . -type f -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" | xargs sed -i 's/MonorepoApp/MeuApp/g'
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp env.example .env
   cp api/env.example api/.env
   cp client/env.example client/.env
   ```

4. **Instale as dependências**
   ```bash
   make setup
   ```

5. **Configure o banco de dados**
   ```bash
   cd api
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Crie um usuário administrador**
   ```bash
   cd api
   flask create-admin
   ```

7. **Inicie o desenvolvimento**
   ```bash
   make dev
   ```

## 🎨 Personalização

### 1. Configurar o Projeto

#### Variáveis de Ambiente

**Arquivo `.env` (raiz):**
```bash
PROJECT_NAME=meu-projeto
APP_NAME=MeuApp
API_URL=http://localhost:8000
CLIENT_URL=http://localhost:5173
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/meu_projeto
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=sua-chave-secreta-aqui
```

**Arquivo `api/.env`:**
```bash
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/meu_projeto
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=sua-chave-secreta-aqui
FRONTEND_URL=http://localhost:5173
```

**Arquivo `client/.env`:**
```bash
VITE_API_URL=http://localhost:8000
VITE_NODE_ENV=development
```

### 2. Personalizar a API

#### Adicionar Novos Modelos

```python
# api/app/domain/models.py
class Product(BaseModel):
    __tablename__ = 'products'
    
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # Relacionamentos
    category = db.relationship('Category', backref='products')
```

#### Criar Repositório

```python
# api/app/infra/repositories/product_repo.py
from .base import BaseRepository
from app.domain.models import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)
    
    def find_by_category(self, category_id: int):
        return self.filter_by(category_id=category_id)
```

#### Criar Serviço

```python
# api/app/api/v1/products/service.py
from app.infra.repositories.product_repo import ProductRepository

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
    
    def get_products(self, category_id: int = None):
        if category_id:
            return self.repo.find_by_category(category_id)
        return self.repo.get_all()
```

#### Criar Rotas

```python
# api/app/api/v1/products/routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from .service import ProductService

products_bp = Blueprint('products', __name__)
service = ProductService()

@products_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    products = service.get_products()
    return jsonify({
        'success': True,
        'data': [product.to_dict() for product in products]
    })
```

#### Registrar Blueprint

```python
# api/app/__init__.py
from app.api.v1.products import products_bp

app.register_blueprint(products_bp, url_prefix='/api/v1/products')
```

### 3. Personalizar o Client

#### Adicionar Nova Feature

```bash
mkdir client/src/features/products
mkdir client/src/features/products/pages
mkdir client/src/features/products/components
```

#### Criar Página

```typescript
// client/src/features/products/pages/ProductsPage.tsx
import React from 'react'
import { useQuery } from 'react-query'
import { apiClient } from '@/lib/apiClient'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/Card'

export const ProductsPage: React.FC = () => {
  const { data, isLoading, error } = useQuery(
    'products',
    () => apiClient.get('/products')
  )

  if (isLoading) return <div>Carregando...</div>
  if (error) return <div>Erro ao carregar produtos</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Produtos</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.data?.map((product: any) => (
          <Card key={product.id}>
            <CardHeader>
              <CardTitle>{product.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">{product.description}</p>
              <p className="text-lg font-semibold">R$ {product.price}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
```

#### Adicionar Rota

```typescript
// client/src/app/App.tsx
import { ProductsPage } from '@/features/products/pages/ProductsPage'

// Adicionar no JSX
<Route path="/products" element={<ProductsPage />} />
```

#### Adicionar ao Menu

```typescript
// client/src/components/Sidebar.tsx
const navigation = [
  // ... outras rotas
  {
    name: 'Produtos',
    href: '/products',
    icon: Package,
  },
]
```

### 4. Personalizar Estilos

#### Adicionar Cores Customizadas

```javascript
// client/tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        }
      }
    }
  }
}
```

#### Criar Componente Customizado

```typescript
// client/src/components/CustomButton.tsx
import React from 'react'
import { Button, ButtonProps } from './Button'

export const CustomButton: React.FC<ButtonProps> = (props) => {
  return (
    <Button
      className="bg-brand-500 hover:bg-brand-600 text-white"
      {...props}
    />
  )
}
```

## 💻 Desenvolvimento

### Comandos Úteis

```bash
# Desenvolvimento completo
make dev

# Apenas API
make dev-api

# Apenas Client
make dev-client

# Build
make build

# Testes
make test

# Linting
make lint

# Docker
make docker-up
make docker-down
```

### Estrutura de Desenvolvimento

1. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Desenvolva no backend primeiro**
   - Crie o modelo
   - Crie o repositório
   - Crie o serviço
   - Crie as rotas
   - Teste com Postman/Insomnia

3. **Desenvolva no frontend**
   - Crie os componentes
   - Crie as páginas
   - Integre com a API
   - Teste a interface

4. **Execute os testes**
   ```bash
   make test
   ```

5. **Execute o linter**
   ```bash
   make lint
   ```

6. **Faça commit**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```

## 🚀 Deploy

### Desenvolvimento

```bash
make docker-up
```

### Produção

1. **Configure as variáveis de ambiente de produção**
   ```bash
   # .env.prod
   FLASK_ENV=production
   DATABASE_URL=postgresql://user:pass@host:5432/database
   REDIS_URL=redis://host:6379/0
   JWT_SECRET_KEY=sua-chave-secreta-de-producao
   FRONTEND_URL=https://seu-dominio.com
   ```

2. **Build das imagens**
   ```bash
   make docker-build
   ```

3. **Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Variáveis de Ambiente de Produção

```bash
# API
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/database
REDIS_URL=redis://host:6379/0
JWT_SECRET_KEY=sua-chave-secreta-de-producao
FRONTEND_URL=https://seu-dominio.com

# Client
VITE_API_URL=https://api.seu-dominio.com
VITE_NODE_ENV=production
```

## 📚 Exemplos

### Exemplo 1: Sistema de Blog

```python
# Modelo de Post
class Post(BaseModel):
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
```

```typescript
// Página de Posts
export const PostsPage: React.FC = () => {
  const { data: posts } = useQuery('posts', () => apiClient.get('/posts'))
  
  return (
    <div className="space-y-6">
      {posts?.data?.map((post: any) => (
        <Card key={post.id}>
          <CardHeader>
            <CardTitle>{post.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{post.content}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

### Exemplo 2: Sistema de E-commerce

```python
# Modelo de Order
class Order(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    items = db.relationship('OrderItem', backref='order')
```

```typescript
// Página de Pedidos
export const OrdersPage: React.FC = () => {
  const { data: orders } = useQuery('orders', () => apiClient.get('/orders'))
  
  return (
    <div className="space-y-4">
      {orders?.data?.map((order: any) => (
        <Card key={order.id}>
          <CardContent>
            <p>Pedido #{order.id}</p>
            <p>Total: R$ {order.total}</p>
            <p>Status: {order.status}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de dependências**
   ```bash
   make clean
   make setup
   ```

2. **Erro de banco de dados**
   ```bash
   cd api
   flask db upgrade
   ```

3. **Erro de CORS**
   - Verifique se `FRONTEND_URL` está correto no `.env` da API

4. **Erro de porta em uso**
   ```bash
   # Encontrar processo usando a porta
   lsof -i :8000
   lsof -i :5173
   
   # Matar processo
   kill -9 <PID>
   ```

### Logs

```bash
# Ver logs do Docker
make docker-logs

# Ver logs da API
cd api && flask logs

# Ver logs do Client
cd client && npm run dev
```

## 📖 Recursos Adicionais

- [README.md](README.md) - Documentação principal
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guia de desenvolvimento
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## 🤝 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a documentação
2. Consulte o [Troubleshooting](#-troubleshooting)
3. Abra uma issue no repositório
4. Entre em contato com a equipe

---

**Monorepo Template** - Guia do Template 🚀

Para começar rapidamente, use o script de setup automático!
