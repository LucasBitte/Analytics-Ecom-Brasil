"""
Script de ingestão de dados - Cria e popula as tabelas no SQL Server
"""

import os
import sys
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# ============================================================
# CONFIGURAÇÃO
# ============================================================

print("=" * 80)
print("INGESTAO DE DADOS - OLISTDB (VERSÃO OTIMIZADA 2.0)")
print("=" * 80)

# Carregar variáveis de ambiente
load_dotenv('.env')

SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_NAME', 'OlistDB')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

print(f"\nServidor: {SERVER}")
print(f"Banco: {DATABASE}")
print(f"Usuario: {USER}")

# Montar string de conexão
odbc_str = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USER};"
    f"PWD={PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
)
connection_url = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

try:
    # Ativação do motor de alta performance para cargas em lote
    engine = create_engine(connection_url, fast_executemany=True)
    with engine.connect() as conn:
        print("\n[OK] Conectado ao banco de dados com fast_executemany=True!")
except Exception as e:
    print(f"\n[ERRO] Falha ao conectar: {e}")
    sys.exit(1)

# ============================================================
# LIMPEZA PREVENTIVA (Derruba na ordem correta de constraints)
# ============================================================
print("\n[PRE-LOAD] Limpando tabelas antigas para evitar conflitos de Foreign Keys...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            DROP TABLE IF EXISTS order_items;
            DROP TABLE IF EXISTS order_payments;
            DROP TABLE IF EXISTS order_reviews;
            DROP TABLE IF EXISTS orders;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS product_categories;
            DROP TABLE IF EXISTS sellers;
            DROP TABLE IF EXISTS customers;
            DROP TABLE IF EXISTS geolocation;
        """))
    print("      [OK] Operação Clean Slate concluída.")
except Exception as e:
    print(f"      [AVISO] Falha ao limpar tabelas: {e}")

# ============================================================
# CRIAR TABELAS
# ============================================================

print("\n" + "=" * 80)
print("CRIANDO TABELAS")
print("=" * 80)

# 1. SELLERS
print("\n[1/9] Criando tabela SELLERS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE sellers (
                seller_id VARCHAR(32) PRIMARY KEY,
                seller_zip_code_prefix INT NOT NULL,
                seller_city VARCHAR(100),
                seller_state CHAR(2)
            );
        """))
    print("      [OK] Tabela SELLERS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 2. CUSTOMERS
print("\n[2/9] Criando tabela CUSTOMERS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE customers (
                customer_id VARCHAR(32) PRIMARY KEY,
                customer_unique_id VARCHAR(32) NOT NULL,
                customer_zip_code_prefix INT NOT NULL,
                customer_city VARCHAR(100),
                customer_state CHAR(2)
            );
        """))
    print("      [OK] Tabela CUSTOMERS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 3. PRODUCTS
print("\n[3/9] Criando tabela PRODUCTS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE products (
                product_id VARCHAR(32) PRIMARY KEY,
                product_category_name VARCHAR(255),
                product_name_lenght SMALLINT NULL,        -- CORRIGIDO: Tipo numérico exato
                product_description_lenght SMALLINT NULL, -- CORRIGIDO: Tipo numérico exato
                product_photos_qty TINYINT NULL,           -- CORRIGIDO: Tipo leve de 1 byte
                product_weight_g FLOAT,
                product_length_cm FLOAT,
                product_height_cm FLOAT,
                product_width_cm FLOAT
            );
        """))
    print("      [OK] Tabela PRODUCTS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 4. GEOLOCATION
print("\n[4/9] Criando tabela GEOLOCATION...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE geolocation (
                geolocation_zip_code_prefix INT PRIMARY KEY,
                geolocation_lat FLOAT,
                geolocation_lng FLOAT,
                geolocation_city VARCHAR(100),
                geolocation_state CHAR(2)
            );
        """))
    print("      [OK] Tabela GEOLOCATION criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 5. PRODUCT_CATEGORIES
print("\n[5/9] Criando tabela PRODUCT_CATEGORIES...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE product_categories (
                product_category_name VARCHAR(255) PRIMARY KEY,
                product_category_name_english VARCHAR(255)
            );
        """))
    print("      [OK] Tabela PRODUCT_CATEGORIES criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 6. ORDERS
print("\n[6/9] Criando tabela ORDERS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE orders (
                order_id VARCHAR(32) PRIMARY KEY,
                customer_id VARCHAR(32) NOT NULL,
                order_status VARCHAR(50),
                order_purchase_timestamp DATETIME,
                order_approved_at DATETIME,
                order_delivered_carrier_date DATETIME,
                order_delivered_customer_date DATETIME,
                order_estimated_delivery_date DATETIME,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            );
        """))
    print("      [OK] Tabela ORDERS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 7. ORDER_ITEMS
print("\n[7/9] Criando tabela ORDER_ITEMS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE order_items (
                order_id VARCHAR(32),
                order_item_id INT,
                product_id VARCHAR(32),
                seller_id VARCHAR(32),
                shipping_limit_date DATETIME,
                price DECIMAL(10,2) NOT NULL,          -- CORRIGIDO: Proteção contra furos financeiros
                freight_value DECIMAL(10,2) NOT NULL,  -- CORRIGIDO: Proteção contra furos financeiros
                PRIMARY KEY (order_id, order_item_id),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
            );
        """))
    print("      [OK] Tabela ORDER_ITEMS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 8. ORDER_PAYMENTS
print("\n[8/9] Criando tabela ORDER_PAYMENTS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE order_payments (
                order_id VARCHAR(32),
                payment_sequential INT,
                payment_type VARCHAR(50),
                payment_installments INT,
                payment_value DECIMAL(10,2) NOT NULL, -- CORRIGIDO: Proteção contra furos financeiros
                PRIMARY KEY (order_id, payment_sequential),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            );
        """))
    print("      [OK] Tabela ORDER_PAYMENTS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# 9. ORDER_REVIEWS
print("\n[9/9] Criando tabela ORDER_REVIEWS...")
try:
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE order_reviews (
                review_id VARCHAR(32) PRIMARY KEY,
                order_id VARCHAR(32),
                review_score INT,
                review_comment_title VARCHAR(200) NULL, -- CORRIGIDO: Otimização de tamanho e indexação
                review_comment_message VARCHAR(MAX),
                review_creation_date DATETIME,
                review_answer_timestamp DATETIME,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            );
        """))
    print("      [OK] Tabela ORDER_REVIEWS criada")
except Exception as e:
    print(f"      [ERRO] {e}")

# ============================================================
# POPULAR TABELAS
# ============================================================

print("\n" + "=" * 80)
print("POPULANDO TABELAS")
print("=" * 80)

# Dicionário com informações das tabelas
tabelas = {
    'sellers': ('data/raw/olist_sellers_dataset.csv', None),
    'customers': ('data/raw/olist_customers_dataset.csv', None),
    'products': ('data/raw/olist_products_dataset.csv', None),
    'geolocation': ('data/raw/olist_geolocation_dataset.csv', None),
    'product_categories': ('data/raw/product_category_name_translation.csv', None),
    'orders': ('data/raw/olist_orders_dataset.csv', ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']),
    'order_items': ('data/raw/olist_order_items_dataset.csv', ['shipping_limit_date']),
    'order_payments': ('data/raw/olist_order_payments_dataset.csv', None),
    'order_reviews': ('data/raw/olist_order_reviews_dataset.csv', ['review_creation_date', 'review_answer_timestamp']),
}

total_geral = 0
for idx, (tabela, (arquivo, date_cols)) in enumerate(tabelas.items(), 1):
    print(f"\n[{idx}/9] Populando tabela {tabela.upper()}...")

    try:
        # Carregar CSV
        df = pd.read_csv(arquivo)

        # Converter colunas de data se necessário
        if date_cols:
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Remover duplicatas baseado na chave primária de cada tabela
        if tabela == 'geolocation':
            df = df.drop_duplicates(subset=['geolocation_zip_code_prefix'])
        elif tabela == 'orders':
            df = df.drop_duplicates(subset=['order_id'])
        elif tabela == 'order_reviews':
            df = df.drop_duplicates(subset=['review_id'])

        # CORREÇÃO CRÍTICA: Transforma NaNs soltos em None para evitar erros de cast no DECIMAL/INT do SQL Server
        df = df.where(pd.notnull(df), None)

        # Inserir no banco em lotes performáticos
        df.to_sql(tabela, engine, if_exists='append', index=False, chunksize=10000)

        total_geral += len(df)
        print(f"      [OK] {len(df):>10,} registros inseridos")

    except Exception as e:
        print(f"      [ERRO] {e}")

# ============================================================
# VALIDAÇÃO E RESUMO
# ============================================================

print("\n" + "=" * 80)
print("VALIDACAO")
print("=" * 80)

try:
    with engine.connect() as conn:
        # Listar tabelas
        result = conn.execute(text("""
            SELECT name FROM sys.tables ORDER BY name
        """))
        tabelas_encontradas = [row[0] for row in result.fetchall()]

        print(f"\n{len(tabelas_encontradas)} tabelas encontradas:\n")
        print(f"{'TABELA':<30} {'REGISTROS':>15}")
        print("-" * 48)

        total = 0
        for tabela in tabelas_encontradas:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {tabela}"))
            count = result.fetchone()[0]
            total += count
            print(f"{tabela:<30} {count:>15,}")

        print("-" * 48)
        print(f"{'TOTAL':<30} {total:>15,}")

        print("\n" + "=" * 80)
        print("RESULTADO FINAL")
        print("=" * 80)
        print(f"\Tabelas criadas: {len(tabelas_encontradas)}")
        print(f"Total de registros: {total:,}")

        if len(tabelas_encontradas) == 9 and total > 400000:
            print("\n[SUCESSO] Ingestao de dados concluida com sucesso!")
        else:
            print("\n[AVISO] Verifique se todas as tabelas foram populadas corretamente")

except Exception as e:
    print(f"\n[ERRO] Falha ao validar: {e}")