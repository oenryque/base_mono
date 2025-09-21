# Monorepo Template - Scripts de Automação
# Template Base para Projetos Full-Stack

.PHONY: help setup dev dev-api dev-client build test lint clean docker-up docker-down docker-logs docker-build

# Cores para output
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(GREEN)Monorepo Template - Scripts Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

setup: ## Instala todas as dependências
	@echo "$(GREEN)🚀 Configurando o monorepo...$(NC)"
	@npm install
	@cd packages/contracts && npm install
	@cd client && npm install
	@cd api && pip install -e .
	@echo "$(GREEN)✅ Setup concluído!$(NC)"

dev: ## Inicia todos os serviços em desenvolvimento
	@echo "$(GREEN)🚀 Iniciando todos os serviços...$(NC)"
	@concurrently "make dev-api" "make dev-client"

dev-api: ## Inicia apenas a API
	@echo "$(GREEN)🔧 Iniciando API Flask...$(NC)"
	@cd api && python manage.py run

dev-client: ## Inicia apenas o Client
	@echo "$(GREEN)💻 Iniciando Client React...$(NC)"
	@cd client && npm run dev

build: ## Build de todos os projetos
	@echo "$(GREEN)🏗️  Fazendo build de todos os projetos...$(NC)"
	@npm run build:contracts
	@npm run build:client
	@echo "$(GREEN)✅ Build concluído!$(NC)"

build-contracts: ## Build dos contratos
	@echo "$(GREEN)📦 Fazendo build dos contratos...$(NC)"
	@cd packages/contracts && npm run build

build-client: ## Build do Client
	@echo "$(GREEN)💻 Fazendo build do Client...$(NC)"
	@cd client && npm run build

test: ## Executa todos os testes
	@echo "$(GREEN)🧪 Executando testes...$(NC)"
	@npm run test

test-client: ## Testes do Client
	@echo "$(GREEN)🧪 Executando testes do Client...$(NC)"
	@cd client && npm run test

lint: ## Executa todos os linters
	@echo "$(GREEN)🔍 Executando linters...$(NC)"
	@npm run lint

lint-client: ## Linter do Client
	@echo "$(GREEN)🔍 Executando linter do Client...$(NC)"
	@cd client && npm run lint

clean: ## Limpa todos os builds
	@echo "$(GREEN)🧹 Limpando builds...$(NC)"
	@npm run clean

clean-client: ## Limpa build do Client
	@echo "$(GREEN)🧹 Limpando build do Client...$(NC)"
	@cd client && rm -rf dist node_modules/.vite

clean-api: ## Limpa build da API
	@echo "$(GREEN)🧹 Limpando build da API...$(NC)"
	@cd api && find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up: ## Inicia serviços com Docker
	@echo "$(GREEN)🐳 Iniciando serviços com Docker...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✅ Serviços iniciados!$(NC)"
	@echo "$(YELLOW)Client: http://localhost:5173$(NC)"
	@echo "$(YELLOW)API: http://localhost:8000$(NC)"

docker-down: ## Para serviços Docker
	@echo "$(GREEN)🐳 Parando serviços Docker...$(NC)"
	@docker-compose down

docker-logs: ## Mostra logs dos serviços
	@echo "$(GREEN)📋 Mostrando logs dos serviços...$(NC)"
	@docker-compose logs -f

docker-build: ## Build das imagens Docker
	@echo "$(GREEN)🐳 Fazendo build das imagens Docker...$(NC)"
	@docker-compose build

# Scripts para setup de novos projetos
setup-new-project: ## Setup para novo projeto (use: make setup-new-project PROJECT_NAME=nome APP_NAME=NomeApp)
	@if [ -z "$(PROJECT_NAME)" ] || [ -z "$(APP_NAME)" ]; then \
		echo "$(RED)❌ Erro: Use make setup-new-project PROJECT_NAME=nome APP_NAME=NomeApp$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)🆕 Configurando novo projeto: $(PROJECT_NAME) - $(APP_NAME)$(NC)"
	@find . -type f \( -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" \) -exec sed -i 's/monorepo-template/$(PROJECT_NAME)/g' {} \;
	@find . -type f \( -name "*.json" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" \) -exec sed -i 's/MonorepoApp/$(APP_NAME)/g' {} \;
	@echo "$(GREEN)✅ Projeto configurado!$(NC)"
	@echo "$(YELLOW)Próximos passos:$(NC)"
	@echo "  1. Edite as variáveis de ambiente em .env, api/.env, client/.env"
	@echo "  2. Configure o banco de dados"
	@echo "  3. Execute: make setup"
	@echo "  4. Execute: make dev"
