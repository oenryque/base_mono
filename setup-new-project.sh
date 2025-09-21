#!/bin/bash

# Script para configurar novo projeto baseado no template
# Uso: ./setup-new-project.sh "nome-do-projeto" "Nome do App"

set -e

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar argumentos
if [ $# -ne 2 ]; then
    echo -e "${RED}❌ Erro: Use ./setup-new-project.sh \"nome-do-projeto\" \"Nome do App\"${NC}"
    echo "Exemplo: ./setup-new-project.sh \"meu-projeto\" \"MeuApp\""
    exit 1
fi

PROJECT_NAME="$1"
APP_NAME="$2"

echo -e "${GREEN}🚀 Configurando novo projeto: $PROJECT_NAME - $APP_NAME${NC}"

# Função para substituir texto em arquivos
replace_in_files() {
    local search="$1"
    local replace="$2"
    local files="$3"
    
    echo "  📝 Atualizando $files..."
    find . -type f \( -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -not -path "./node_modules/*" -not -path "./.git/*" -exec sed -i "s/$search/$replace/g" {} \;
}

# Substituir nomes nos arquivos
echo -e "${YELLOW}📝 Atualizando nomes nos arquivos...${NC}"
replace_in_files "monorepo-template" "$PROJECT_NAME" "arquivos de configuração"
replace_in_files "MonorepoApp" "$APP_NAME" "nomes de aplicação"

# Atualizar package.json raiz
echo -e "${YELLOW}📦 Atualizando package.json raiz...${NC}"
sed -i "s/\"name\": \"monorepo-template\"/\"name\": \"$PROJECT_NAME\"/" package.json
sed -i "s/\"description\": \"Template Base para Projetos Full-Stack - Monorepo completo com API Flask e Client React\"/\"description\": \"$APP_NAME - Projeto baseado no Monorepo Template\"/" package.json

# Atualizar README.md
echo -e "${YELLOW}📚 Atualizando README.md...${NC}"
sed -i "s/# Monorepo Template 🚀/# $APP_NAME 🚀/" README.md
sed -i "s/**Template Base para Projetos Full-Stack** - Monorepo completo com API Flask e Client React/**$APP_NAME** - Projeto baseado no Monorepo Template/" README.md

# Atualizar docker-compose.yml
echo -e "${YELLOW}🐳 Atualizando docker-compose.yml...${NC}"
sed -i "s/monorepo_template/${PROJECT_NAME//-/_}/g" docker-compose.yml
sed -i "s/monorepo-db/${PROJECT_NAME}-db/g" docker-compose.yml
sed -i "s/monorepo-redis/${PROJECT_NAME}-redis/g" docker-compose.yml
sed -i "s/monorepo-api/${PROJECT_NAME}-api/g" docker-compose.yml
sed -i "s/monorepo-client/${PROJECT_NAME}-client/g" docker-compose.yml
sed -i "s/monorepo-network/${PROJECT_NAME}-network/g" docker-compose.yml

# Atualizar variáveis de ambiente
echo -e "${YELLOW}🔧 Atualizando variáveis de ambiente...${NC}"
sed -i "s/monorepo_template/${PROJECT_NAME//-/_}/g" env.example
sed -i "s/monorepo-template/$PROJECT_NAME/g" env.example
sed -i "s/MonorepoApp/$APP_NAME/g" env.example

# Atualizar API
echo -e "${YELLOW}🔧 Atualizando configurações da API...${NC}"
sed -i "s/monorepo-api/$PROJECT_NAME-api/g" api/pyproject.toml
sed -i "s/monorepo_template/${PROJECT_NAME//-/_}/g" api/env.example
sed -i "s/monorepo_template/${PROJECT_NAME//-/_}/g" api/app/config.py

# Atualizar Client
echo -e "${YELLOW}💻 Atualizando configurações do Client...${NC}"
sed -i "s/monorepo-client/$PROJECT_NAME-client/g" client/package.json

# Criar arquivo .env baseado no exemplo
echo -e "${YELLOW}📄 Criando arquivo .env...${NC}"
cp env.example .env

# Atualizar .env com valores específicos do projeto
sed -i "s/your-super-secret-jwt-key-change-in-production/$(openssl rand -hex 32)/g" .env
sed -i "s/your-super-secret-key-change-in-production/$(openssl rand -hex 32)/g" .env

# Criar .env para API
echo -e "${YELLOW}📄 Criando .env para API...${NC}"
cp api/env.example api/.env

# Criar .env para Client
echo -e "${YELLOW}📄 Criando .env para Client...${NC}"
cp client/env.example client/.env

# Atualizar .gitignore se necessário
echo -e "${YELLOW}📝 Verificando .gitignore...${NC}"
if ! grep -q "\.env" .gitignore; then
    echo ".env" >> .gitignore
    echo ".env.local" >> .gitignore
    echo ".env.production" >> .gitignore
fi

# Criar diretório de logs
echo -e "${YELLOW}📁 Criando diretórios necessários...${NC}"
mkdir -p logs
mkdir -p api/logs
mkdir -p client/dist

# Tornar scripts executáveis
echo -e "${YELLOW}🔧 Configurando permissões...${NC}"
chmod +x setup-new-project.sh
chmod +x setup-new-project.ps1

echo -e "${GREEN}✅ Projeto configurado com sucesso!${NC}"
echo ""
echo -e "${YELLOW}📋 Próximos passos:${NC}"
echo "  1. Instale as dependências: make setup"
echo "  2. Configure o banco de dados: cd api && flask db init && flask db migrate -m 'Initial migration' && flask db upgrade"
echo "  3. Crie um usuário administrador: cd api && flask create-admin"
echo "  4. Inicie o desenvolvimento: make dev"
echo "  5. Acesse: http://localhost:5173 (Client) e http://localhost:8000 (API)"
echo ""
echo -e "${YELLOW}📚 Documentação:${NC}"
echo "  - README.md: Guia principal"
echo "  - DEVELOPMENT.md: Guia de desenvolvimento"
echo "  - API Docs: http://localhost:8000/api/docs"
echo ""
echo -e "${GREEN}🎉 Seu projeto $APP_NAME está pronto para desenvolvimento!${NC}"
