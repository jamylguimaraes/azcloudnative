## 📘 Introdução

Neste projeto, vamos criar e publicar um **blog básico** usando **Docker** e **Azure Container Apps**.

---

## 🐳 Etapa 1 – Criando o Dockerfile

Vamos usar como exemplo o arquivo index.html, mas o processo funciona com qualquer framework.

### ✅ 1. Estrutura do Projeto

```
  ├── index.html
  ├── deployment.yaml
  ├── service.yaml
  └── Dockerfile
```

---

## ☁️ Etapa 2 – Criando o Resource Group e Container Registry no Azure

### ✅ 1. Criar o Resource Group

```bash
az group create --name rg-blog-app --location brazilsouth
```

### ✅ 2. Criar o Azure Container Registry (ACR)

```bash
az acr create --resource-group rg-blog-app --name blogregistry001 --sku Basic --admin-enabled true
```

Anote o **login server** (ex: `blogregistry001.azurecr.io`).

### ✅ 3. Fazer login no ACR localmente

```bash
az acr login --name blogregistry001
```

---

## 🐳 Etapa 3 – Build e Push da Imagem no ACR

### ✅ 1. Build da imagem localmente

```bash
docker build -t blogregistry001.azurecr.io/blog-app:v1 .
```

### ✅ 2. Push para o ACR

```bash
docker push blogregistry001.azurecr.io/blog-app:v1
```

---

## 🚀 Etapa 4 – Criando o Azure Container App

### ✅ 1. Registrar o ambiente

Crie o ambiente de execução (se ainda não existir):

```bash
az containerapp env create \
  --name blog-env \
  --resource-group rg-blog-app \
  --location brazilsouth
```

### ✅ 2. Criar o Container App com imagem do ACR

```bash
az containerapp create \
  --name blog-app \
  --resource-group rg-blog-app \
  --environment blog-env \
  --image blogregistry001.azurecr.io/blog-app:v1 \
  --target-port 8080 \
  --ingress external \
  --registry-server blogregistry001.azurecr.io \
  --registry-username $(az acr credential show --name blogregistry001 --query username -o tsv) \
  --registry-password $(az acr credential show --name blogregistry001 --query passwords[0].value -o tsv)
```

---

## ✅ Etapa 5 – Finalizando o Projeto

Após a criação:

1. O Azure vai gerar uma URL pública (ex: `https://blog-app.<hash>.azurecontainerapps.io`)
2. Acesse essa URL no navegador para ver seu blog rodando



