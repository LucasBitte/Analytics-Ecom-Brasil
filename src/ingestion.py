import os
import shutil
import kagglehub

def download_olist_dataset():
    """Baixa o dataset da Olist via kagglehub e move para data/raw/"""
    print("⏳ Iniciando o download do dataset da Olist via KaggleHub...")
    
    # 1. Baixa o dataset (ele vai para a pasta de cache padrão do kagglehub)
    cache_dir = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    print(f"✅ Download concluído! Arquivos baixados em: {cache_dir}")
    
    # 2. Define o caminho de destino do nosso projeto
    target_dir = os.path.join("data", "raw")
    os.makedirs(target_dir, exist_ok=True)
    
    # 3. Move/Copia os arquivos .csv da pasta cache para data/raw
    print("🚚 Organizando os arquivos na pasta data/raw/...")
    files = os.listdir(cache_dir)
    csv_count = 0
    
    for file in files:
        if file.endswith('.csv'):
            source_file = os.path.join(cache_dir, file)
            target_file = os.path.join(target_dir, file)
            
            # Copia o arquivo para a nossa pasta local
            shutil.copy(source_file, target_file)
            print(f"  -> {file} movido com sucesso!")
            csv_count += 1
            
    print(f"\n🎉 Sucesso! {csv_count} arquivos brutos (.csv) estão prontos em '{target_dir}'.")

if __name__ == "__main__":
    download_olist_dataset()