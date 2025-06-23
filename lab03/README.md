* Criação de App Service para hospedar a API
* Criação do Azure API Management
* Exposição de endpoints com boas práticas
* Configuração de **autenticação com JWT**

---

##  Etapa 1 – Estrutura do Projeto

* Uma API REST (ex: em Flask, Node.js, .NET etc.)
* Endpoint `/pagamentos`
* JWT gerado por um provedor confiável

---

##  Etapa 2 – Criando App Service (hospedagem da API)

### ✅ 1. Criar Grupo de Recursos

```bash
az group create --name rg-pagamentos --location brazilsouth
```

### ✅ 2. Criar App Service Plan

```bash
az appservice plan create \
  --name plan-pagamento-api \
  --resource-group rg-pagamentos \
  --sku B1 --is-linux
```

### ✅ 3. Criar App Service (Web App)

```bash
az webapp create \
  --resource-group rg-pagamentos \
  --plan plan-pagamento-api \
  --name pagamento-api001 \
  --runtime "PYTHON:3.11" \
  --deployment-local-git
```

> Você receberá uma URL do Git para `git push` direto sua API.

---

## Etapa 3 – Criando API Management (APIM)

### ✅ 1. Criar instância do API Management

```bash
az apim create \
  --name apim-pagamentos \
  --resource-group rg-pagamentos \
  --publisher-name "SuaEmpresa" \
  --publisher-email "seu@email.com" \
  --location brazilsouth \
  --sku-name Consumption
```

> O SKU *Consumption* é **gratuito e sem servidor**, ideal para APIs com baixo volume inicial.

---

## 🔄 Etapa 4 – Importando sua API para o API Management

### ✅ 1. Criar API manualmente apontando para o App Service

```bash
az apim api create \
  --resource-group rg-pagamentos \
  --service-name apim-pagamentos \
  --api-id pagamento-api \
  --path pagamentos \
  --display-name "API de Pagamentos" \
  --protocols https \
  --service-url https://pagamento-api001.azurewebsites.net
```

---

## Etapa 5 – Endpoints

### ✅ Criar operação "POST /pagamentos"

```bash
az apim api operation create \
  --resource-group rg-pagamentos \
  --service-name apim-pagamentos \
  --api-id pagamento-api \
  --operation-id postPagamento \
  --display-name "Registrar pagamento" \
  --method POST \
  --url-template "/pagamentos" \
  --request-description "Registrar novo pagamento" \
  --response-status-code 201
```

---

##  Etapa 6 – Configurando autenticação com JWT

### ✅ 1. Criar política de validação JWT no API Management

Política XML do APIM para validar o JWT

```xml
<validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Token inválido">
    <openid-config url="https://<PROVEDOR_OIDC>/.well-known/openid-configuration" />
    <audiences>
        <audience>api-pagamento</audience>
    </audiences>
</validate-jwt>
```

Salvar como `jwt-policy.xml`.

### ✅ 2. Aplicar a política de JWT ao endpoint da API

```bash
az apim api operation policy update \
  --resource-group rg-pagamentos \
  --service-name apim-pagamentos \
  --api-id pagamento-api \
  --operation-id postPagamento \
  --xml-content "$(cat jwt-policy.xml)"
```

---

## Etapa 7 – Testando

* Obtenha um JWT do seu provedor
* Envie um `POST /pagamentos` para a URL do APIM, com header:

```http
Authorization: Bearer <seu_token_jwt>
```

---

## ✅ Resultado final

* **API hospedada** no Azure App Service
* **Gerenciada com segurança** no Azure API Management
* **Protegida com JWT**
* **Pronta para escalar com controle de acesso, logs e versionamento**

