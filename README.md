# ContractWeb API - Testes Automatizados

Projeto de testes automatizados para a API ContractWeb usando Python, Pytest e Playwright.

## 📋 Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Executando os Testes](#executando-os-testes)
- [Relatórios](#relatórios)
- [CI/CD](#cicd)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🔧 Requisitos

- Python 3.11+
- pip
- Git

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd automation_test_cweb_api
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium
```

## ⚙️ Configuração

1. Copie o arquivo `env.example` para `.env`:
```bash
cp env.example .env
```

2. Edite o arquivo `.env` com suas configurações:
```env
BASE_URL=https://contractwebapi.preprod.bernhoeft.com.br
API_VERSION=v1
TIMEOUT=30
API_KEY=your_api_key_here
```

## 🚀 Executando os Testes

### Executar todos os testes:
```bash
pytest
```

### Executar testes específicos:
```bash
# Por arquivo
pytest tests/test_area.py

# Por marcador
pytest -m smoke
pytest -m api
pytest -m regression

# Por palavra-chave
pytest -k "test_get"
```

### Executar com mais verbosidade:
```bash
pytest -v
pytest -vv  # Mais detalhado
```

### Executar com saída de print statements:
```bash
pytest -s
```

## 📊 Relatórios

### Relatório HTML do Pytest:
```bash
pytest --html=reports/report.html --self-contained-html
```
O relatório será gerado em `reports/report.html`

### Relatório Allure:

1. Gerar resultados do Allure:
```bash
pytest --alluredir=allure-results
```

2. Gerar relatório HTML do Allure:
```bash
allure generate allure-results -o allure-report --clean
```

3. Abrir relatório no navegador:
```bash
allure open allure-report
```

### Relatório Allure no servidor:
```bash
allure serve allure-results
```

## 🔄 CI/CD

O projeto está configurado para executar automaticamente no Bitbucket Pipelines.

### Configuração do Bitbucket Pipelines

O arquivo `bitbucket-pipelines.yml` está configurado para:
1. Instalar dependências
2. Executar todos os testes
3. Gerar relatórios Allure
4. Publicar artefatos

### Executar pipeline localmente (opcional):
```bash
# Instalar bitbucket-pipelines-runner (se disponível)
# ou usar Docker para simular o ambiente
```

## 📁 Estrutura do Projeto

```
automation_test_cweb_api/
├── tests/                          # Testes automatizados
│   ├── __init__.py
│   ├── test_amostragem_grupo_area.py
│   ├── test_area.py
│   ├── test_events.py
│   └── test_all_endpoints.py       # Testes para todos os endpoints
├── utils/                          # Utilitários
│   ├── api_client.py               # Cliente HTTP para APIs
│   └── helpers.py                  # Funções auxiliares
├── config.py                       # Configurações
├── conftest.py                     # Fixtures do Pytest
├── requirements.txt               # Dependências Python
├── pytest.ini                     # Configuração do Pytest
├── .env.example                    # Exemplo de variáveis de ambiente
├── .gitignore                     # Arquivos ignorados pelo Git
├── bitbucket-pipelines.yml        # Configuração CI/CD
└── README.md                      # Este arquivo
```

## 🏷️ Marcadores de Teste

O projeto usa marcadores do Pytest para categorizar os testes:

- `@pytest.mark.smoke` - Testes de smoke (críticos)
- `@pytest.mark.regression` - Testes de regressão
- `@pytest.mark.api` - Testes de API
- `@pytest.mark.critical` - Testes críticos

### Executar por marcador:
```bash
pytest -m smoke          # Apenas smoke tests
pytest -m "smoke or api" # Smoke ou API tests
pytest -m "not critical" # Todos exceto critical
```

## 📝 Endpoints Testados

O projeto testa todos os endpoints da API ContractWeb:

- **AmostragemGrupoArea**: CRUD completo
- **Area**: CRUD completo
- **Avisos**: CRUD + endpoints específicos
- **ClassificacaoColaborador**: CRUD completo
- **Contratada**: CRUD + PATCH
- **ContratadaContrato**: CRUD completo
- **Contratante**: CRUD + endpoints relacionados
- **Contrato**: CRUD + endpoints relacionados
- **Events**: Criação de eventos e pre-processamento
- **Familia**: CRUD completo
- **GrupoArea**: CRUD + endpoints relacionados
- **GrupoContratante**: CRUD completo
- **GrupoFaturamento**: CRUD + Faixa Faturamento
- **LocalServico**: CRUD completo
- **ObjetoAnalise**: CRUD completo
- **ObjetoAnaliseTipoEspecifico**: CRUD completo
- **ObjetoOficial**: CRUD completo
- **Operador**: CRUD + vínculos
- **Parametros**: Endpoints de parâmetros
- **PerfilAcesso**: Leitura de perfis
- **Risco**: CRUD completo
- **SubFamilia**: CRUD completo
- **Suporte**: Gerenciamento de cartilha
- **UnidadeContratante**: CRUD completo
- **VideoCast**: Leitura + callback

## 🐛 Troubleshooting

### Erro ao instalar Playwright:
```bash
playwright install chromium
playwright install-deps chromium
```

### Erro de importação:
Certifique-se de que o ambiente virtual está ativado e todas as dependências estão instaladas.

### Erro de autenticação:
Verifique se o `API_KEY` está configurado corretamente no arquivo `.env`.

## 📚 Recursos Adicionais

- [Documentação do Pytest](https://docs.pytest.org/)
- [Documentação do Playwright](https://playwright.dev/python/)
- [Documentação do Allure](https://docs.qameta.io/allure/)
- [Documentação da API ContractWeb](https://contractwebapi.preprod.bernhoeft.com.br/index.html)

## 👥 Contribuindo

1. Crie uma branch para sua feature
2. Faça suas alterações
3. Execute os testes
4. Crie um Pull Request

## 📄 Licença

Este projeto é para uso interno da equipe de QA.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato com a equipe de QA.