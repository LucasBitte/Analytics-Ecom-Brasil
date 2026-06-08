import os
import pandas as pd
from sqlalchemy import text
# Importa a função de conexão que testamos e validamos com sucesso
from database import get_engine 

# Nome do banco de dados dedicado ao projeto
RAW_DB_NAME = "ANALYTICS_ECOM_RAW"

def create_raw_database():
    """Garante a criação do banco de dados para os dados brutos se não existir"""
    print(f"🛠️ Verificando existência do banco de dados [{RAW_DB_NAME}]...")
    engine = get_engine()
    
    # Execuções de criação de banco não podem rodar dentro de transações abertas no SQL Server
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        # Verifica se o banco já existe
        db_exists = conn.execute(
            text(f"SELECT 1 FROM sys.databases WHERE name = '{RAW_DB_NAME}'")
        ).fetchone()
        
        if not db_exists:
            conn.execute(text(f"CREATE DATABASE {RAW_DB_NAME}"))
            print(f"✨ Banco de dados [{RAW_DB_NAME}] criado com sucesso!")
        else:
            print(f"📦 Banco de dados [{RAW_DB_NAME}] já existe. Prosseguindo...")

def ingest_csv_to_sql():
    """Lê os CSVs da pasta data/raw e insere no banco ANALYTICS_ECOM_RAW"""
    raw_dir = os.path.join("data", "raw")
    
    if not os.path.exists(raw_dir) or not os.listdir(raw_dir):
        print("❌ Erro: A pasta 'data/raw' está vazia ou não existe. Execute o download primeiro.")
        return

    # Cria o motor de conexão apontando especificamente para o novo banco criado
    engine = get_engine()
    # Modifica dinamicamente a string de conexão para apontar para o nosso banco definitivo
    target_connection_url = engine.url.set(database=RAW_DB_NAME)
    target_engine = get_engine().__class__(target_connection_url, fast_executemany=True)

    print("\n🚀 Iniciando a ingestão dos dados no SQL Server...")
    
    for file in os.listdir(raw_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(raw_dir, file)
            
            # Define o nome da tabela no SQL removendo o '.csv' e limpando o sufixo '_dataset'
            table_name = file.replace(".csv", "").replace("_dataset", "")
            
            print(f"⏳ Carregando {file} para a tabela [{table_name}]...")
            
            # Lê o CSV usando Pandas
            df = pd.read_csv(file_path)
            
            # Grava no SQL Server (substitui a tabela se ela já existir)
            df.to_sql(
                name=table_name,
                con=target_engine,
                if_exists="replace",
                index=False,
                chunksize=5000 # Envia em blocos de 5000 para otimizar a memória
            )
            
            print(f"✅ Tabela [{table_name}] populada com sucesso! ({len(df)} linhas)")

if __name__ == "__main__":
    # Passo 1: Garantir que o banco de dados existe
    create_raw_database()
    # Passo 2: Fazer a carga dos arquivos brutos
    ingest_csv_to_sql()
    print("\n🎉 ETAPA DE INGESTÃO CONCLUÍDA COM SUCESSO NO SEU BANCO LOCAL!")