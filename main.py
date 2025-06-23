import streamlit as st
from azure.storage.blob import BlobServiceClient
import pymssql
import uuid
import json
import os
import pandas as pd

# Configurações globais
AZURE_STORAGE = {
    "connection_string": "DefaultEndpointsProtocol=https;AccountName=azcloudnativejamlab01;AccountKey=w/jdjdjhjkdhkjdhfjdhkjdhd==;EndpointSuffix=core.windows.net",
    "container_name": "produtos",
    "account_name": "azcloudnativejamlab01"
}

AZURE_SQL = {
    "server": "azcloudnativejamlab01.database.windows.net",
    "database": "lab001",
    "username": "adminlab",
    "password": "labq1w2e3r4"
}

# Título
st.title("Cadastro de Produto - E-Commerce na Cloud")

# Formulário
nome = st.text_input("Nome do Produto")
descricao = st.text_area("Descrição do Produto")
preco = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
imagem = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

# Envia a imagem para o Blob Storage
def enviar_imagem(file):
    try:
        blob_service = BlobServiceClient.from_connection_string(AZURE_STORAGE["connection_string"])
        blob_client = blob_service.get_container_client(AZURE_STORAGE["container_name"])
        nome_blob = f"{uuid.uuid4()}.jpg"
        blob = blob_client.get_blob_client(nome_blob)
        blob.upload_blob(file.read(), overwrite=True)
        return f"https://{AZURE_STORAGE['account_name']}.blob.core.windows.net/{AZURE_STORAGE['container_name']}/{nome_blob}"
    except Exception as e:
        st.error(f"Erro ao enviar imagem: {e}")
