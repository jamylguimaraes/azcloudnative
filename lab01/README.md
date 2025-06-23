## 📘 Introdução

Neste projeto, você criará uma aplicação de cadastro de produtos usando **Streamlit** com backend na **Azure Cloud**. O app permitirá:

* Cadastro de produtos com nome, descrição, preço e imagem.
* Armazenamento das imagens no **Azure Blob Storage**.
* Armazenamento das informações no **Azure SQL Database**.
* Exibição dos produtos cadastrados.

---

## 🔹 Etapa 1 – Criando um Resource Group e SQL Database

### ✅ 1. Criar o Resource Group

No portal do Azure ou via CLI:

**Via Portal Azure:**

* Acesse "Resource Groups" > "Criar".
* Nome: `rg-ecommerce`
* Região: `Brazil South` ou a mais próxima de você.

**Via CLI:**

```bash
az group create --name rg-ecommerce --location brazilsouth
```
### ✅ 2. Criar o Azure SQL Server + Banco de Dados

**Via Portal:**

* Acesse "SQL Databases" > "Criar".
* Nome do banco: `lab001`
* Nome do servidor: `azcloudnativejamlab01`
* Login do administrador: `adminlab`
* Senha: `labq1w2e3r4`
* Grupo de recursos: `rg-ecommerce`
* Plano de preço: Comece com **Basic**.

**Via CLI:**

```bash
# Criar servidor
az sql server create \
  --name azcloudnativejamlab01 \
  --resource-group rg-ecommerce \
  --location brazilsouth \
  --admin-user adminlab \
  --admin-password labq1w2e3r4

# Criar banco de dados
az sql db create \
  --resource-group rg-ecommerce \
  --server azcloudnativejamlab01 \
  --name lab001 \
  --service-objective Basic
```

### ✅ 3. Liberar o acesso à sua máquina local

Adicione seu IP nas regras de firewall:

```bash
az sql server firewall-rule create \
  --resource-group rg-ecommerce \
  --server azcloudnativejamlab01 \
  --name AllowLocalAccess \
  --start-ip-address YOUR_IP \
  --end-ip-address YOUR_IP
```

---

## 🔹 Etapa 2 – Criando uma Storage Account

### ✅ 1. Criar a Storage Account

**Via Portal:**

* Vá em "Storage accounts" > "Criar".
* Nome: `azcloudnativejamlab01`
* Tipo: `StorageV2 (general purpose v2)`
* Replicação: `LRS`
* Grupo de Recursos: `rg-ecommerce`

**Via CLI:**

```bash
az storage account create \
  --name azcloudnativejamlab01 \
  --resource-group rg-ecommerce \
  --location brazilsouth \
  --sku Standard_LRS \
  --kind StorageV2
```

### ✅ 2. Criar o Container Blob

**Via Portal:**

* Vá em sua storage account > "Containers" > "Criar".
* Nome do container: `produtos`
* Nível de acesso: Público (somente leitura de blobs).

**Via CLI:**

```bash
az storage container create \
  --name produtos \
  --account-name azcloudnativejamlab01 \
  --public-access blob
```

---

## 🔹 Etapa 3 – Configurando o Banco de Dados e Criando a Tabela

Você pode usar o **Azure Data Studio**, **SSMS** ou **pymssql** para executar o seguinte script SQL:

```sql
CREATE TABLE dbo.Produtos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nome NVARCHAR(255) NOT NULL,
    descricao NVARCHAR(MAX),
    preco DECIMAL(10, 2),
    imagem_url NVARCHAR(500)
);
```

---

## 🔹 Etapa 4 – Implementando o Salvamento de Imagens no Blob

O código já está configurado para:

* Gerar um nome único com `uuid4()`.
* Fazer upload para o Blob Storage com `BlobServiceClient`.
* Construir a URL de acesso.

Certifique-se de:

✅ Instalar as bibliotecas:

```bash
pip install streamlit azure-storage-blob pymssql pandas
```

✅ Ter a **connection string** da sua storage account (no portal: > Access keys > `Connection string`).

---

## 🔹 Etapa 5 – Finalizando o Projeto

### ✅ 1. Testar localmente

Execute seu app com:

```bash
streamlit run app.py
```

Verifique:

* O cadastro funciona?
* As imagens estão sendo salvas no Blob?
* Os dados aparecem corretamente?

### ✅ 2. Publicar (opcional)

Você pode hospedar o app no:

* **Azure App Service (Linux, Python 3.11)**
* **Azure Container Apps** (caso você conteinerize com Docker)
* **Streamlit Cloud** (teste gratuito)

---

## ✅ Checklist Final

| Item                          | Status |
| ----------------------------- | ------ |
| Resource Group criado         | ✅      |
| SQL Server e Database         | ✅      |
| Storage Account + Container   | ✅      |
| Tabela no SQL criada          | ✅      |
| Código funcionando localmente | ✅      |


