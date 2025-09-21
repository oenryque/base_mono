# Script PowerShell para configurar novo projeto baseado no template
# Uso: .\setup-new-project.ps1 -ProjectName "nome-do-projeto" -AppName "Nome do App"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$true)]
    [string]$AppName
)

# Cores para output
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$NC = "`e[0m"

Write-Host "${Green}🚀 Configurando novo projeto: $ProjectName - $AppName${NC}"

# Função para substituir texto em arquivos
function Replace-InFiles {
    param(
        [string]$Search,
        [string]$Replace,
        [string]$Description
    )
    
    Write-Host "  📝 Atualizando $Description..." -ForegroundColor Yellow
    
    $files = Get-ChildItem -Recurse -Include "*.json", "*.md", "*.yml", "*.yaml", "*.py", "*.ts", "*.tsx", "*.js", "*.jsx" | 
             Where-Object { $_.FullName -notlike "*node_modules*" -and $_.FullName -notlike "*.git*" }
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        $content = $content -replace [regex]::Escape($Search), $Replace
        Set-Content $file.FullName -Value $content -NoNewline
    }
}

try {
    # Substituir nomes nos arquivos
    Write-Host "${Yellow}📝 Atualizando nomes nos arquivos...${NC}"
    Replace-InFiles "monorepo-template" $ProjectName "arquivos de configuração"
    Replace-InFiles "MonorepoApp" $AppName "nomes de aplicação"

    # Atualizar package.json raiz
    Write-Host "${Yellow}📦 Atualizando package.json raiz...${NC}"
    $packageJson = Get-Content "package.json" -Raw
    $packageJson = $packageJson -replace '"name": "monorepo-template"', "`"name`": `"$ProjectName`""
    $packageJson = $packageJson -replace '"description": "Template Base para Projetos Full-Stack - Monorepo completo com API Flask e Client React"', "`"description`": `"$AppName - Projeto baseado no Monorepo Template`""
    Set-Content "package.json" -Value $packageJson -NoNewline

    # Atualizar README.md
    Write-Host "${Yellow}📚 Atualizando README.md...${NC}"
    $readme = Get-Content "README.md" -Raw
    $readme = $readme -replace "# Monorepo Template 🚀", "# $AppName 🚀"
    $readme = $readme -replace "\*\*Template Base para Projetos Full-Stack\*\* - Monorepo completo com API Flask e Client React", "**$AppName** - Projeto baseado no Monorepo Template"
    Set-Content "README.md" -Value $readme -NoNewline

    # Atualizar docker-compose.yml
    Write-Host "${Yellow}🐳 Atualizando docker-compose.yml...${NC}"
    $dockerCompose = Get-Content "docker-compose.yml" -Raw
    $projectNameUnderscore = $ProjectName -replace "-", "_"
    $dockerCompose = $dockerCompose -replace "monorepo_template", $projectNameUnderscore
    $dockerCompose = $dockerCompose -replace "monorepo-db", "$ProjectName-db"
    $dockerCompose = $dockerCompose -replace "monorepo-redis", "$ProjectName-redis"
    $dockerCompose = $dockerCompose -replace "monorepo-api", "$ProjectName-api"
    $dockerCompose = $dockerCompose -replace "monorepo-client", "$ProjectName-client"
    $dockerCompose = $dockerCompose -replace "monorepo-network", "$ProjectName-network"
    Set-Content "docker-compose.yml" -Value $dockerCompose -NoNewline

    # Atualizar variáveis de ambiente
    Write-Host "${Yellow}🔧 Atualizando variáveis de ambiente...${NC}"
    $envExample = Get-Content "env.example" -Raw
    $envExample = $envExample -replace "monorepo_template", $projectNameUnderscore
    $envExample = $envExample -replace "monorepo-template", $ProjectName
    $envExample = $envExample -replace "MonorepoApp", $AppName
    Set-Content "env.example" -Value $envExample -NoNewline

    # Atualizar API
    Write-Host "${Yellow}🔧 Atualizando configurações da API...${NC}"
    $pyproject = Get-Content "api/pyproject.toml" -Raw
    $pyproject = $pyproject -replace "monorepo-api", "$ProjectName-api"
    Set-Content "api/pyproject.toml" -Value $pyproject -NoNewline

    $apiEnv = Get-Content "api/env.example" -Raw
    $apiEnv = $apiEnv -replace "monorepo_template", $projectNameUnderscore
    Set-Content "api/env.example" -Value $apiEnv -NoNewline

    $config = Get-Content "api/app/config.py" -Raw
    $config = $config -replace "monorepo_template", $projectNameUnderscore
    Set-Content "api/app/config.py" -Value $config -NoNewline

    # Atualizar Client
    Write-Host "${Yellow}💻 Atualizando configurações do Client...${NC}"
    $clientPackage = Get-Content "client/package.json" -Raw
    $clientPackage = $clientPackage -replace "monorepo-client", "$ProjectName-client"
    Set-Content "client/package.json" -Value $clientPackage -NoNewline

    # Criar arquivo .env baseado no exemplo
    Write-Host "${Yellow}📄 Criando arquivo .env...${NC}"
    Copy-Item "env.example" ".env"

    # Gerar chaves secretas
    $jwtSecret = -join ((1..32) | ForEach {Get-Random -InputObject (0..9 + 'A'..'F')})
    $appSecret = -join ((1..32) | ForEach {Get-Random -InputObject (0..9 + 'A'..'F')})

    # Atualizar .env com valores específicos do projeto
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace "your-super-secret-jwt-key-change-in-production", $jwtSecret
    $envContent = $envContent -replace "your-super-secret-key-change-in-production", $appSecret
    Set-Content ".env" -Value $envContent -NoNewline

    # Criar .env para API
    Write-Host "${Yellow}📄 Criando .env para API...${NC}"
    Copy-Item "api/env.example" "api/.env"

    # Atualizar API .env com chaves
    $apiEnvContent = Get-Content "api/.env" -Raw
    $apiEnvContent = $apiEnvContent -replace "your-super-secret-jwt-key-change-in-production", $jwtSecret
    $apiEnvContent = $apiEnvContent -replace "your-super-secret-key-change-in-production", $appSecret
    Set-Content "api/.env" -Value $apiEnvContent -NoNewline

    # Criar .env para Client
    Write-Host "${Yellow}📄 Criando .env para Client...${NC}"
    Copy-Item "client/env.example" "client/.env"

    # Atualizar .gitignore se necessário
    Write-Host "${Yellow}📝 Verificando .gitignore...${NC}"
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -notmatch "\.env") {
        Add-Content ".gitignore" "`n.env`n.env.local`n.env.production"
    }

    # Criar diretórios necessários
    Write-Host "${Yellow}📁 Criando diretórios necessários...${NC}"
    New-Item -ItemType Directory -Force -Path "logs" | Out-Null
    New-Item -ItemType Directory -Force -Path "api/logs" | Out-Null
    New-Item -ItemType Directory -Force -Path "client/dist" | Out-Null

    Write-Host "${Green}✅ Projeto configurado com sucesso!${NC}"
    Write-Host ""
    Write-Host "${Yellow}📋 Próximos passos:${NC}"
    Write-Host "  1. Instale as dependências: make setup"
    Write-Host "  2. Configure o banco de dados: cd api && flask db init && flask db migrate -m 'Initial migration' && flask db upgrade"
    Write-Host "  3. Crie um usuário administrador: cd api && flask create-admin"
    Write-Host "  4. Inicie o desenvolvimento: make dev"
    Write-Host "  5. Acesse: http://localhost:5173 (Client) e http://localhost:8000 (API)"
    Write-Host ""
    Write-Host "${Yellow}📚 Documentação:${NC}"
    Write-Host "  - README.md: Guia principal"
    Write-Host "  - DEVELOPMENT.md: Guia de desenvolvimento"
    Write-Host "  - API Docs: http://localhost:8000/api/docs"
    Write-Host ""
    Write-Host "${Green}🎉 Seu projeto $AppName está pronto para desenvolvimento!${NC}"

} catch {
    Write-Host "${Red}❌ Erro ao configurar projeto: $($_.Exception.Message)${NC}"
    exit 1
}
