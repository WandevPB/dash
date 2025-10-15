"""
Script para converter CSV em Parquet comprimido
Formato ideal para Streamlit Cloud - menor e mais rápido
"""

import pandas as pd
import os

def criar_parquet():
    """Converte CSV consolidado em Parquet comprimido"""
    
    print("🔄 Iniciando conversão para Parquet...")
    
    # Caminhos
    csv_path = 'dados/dados_consolidados_2025.csv'
    parquet_path = 'dados/inventario.parquet'
    
    # Verificar se CSV existe
    if not os.path.exists(csv_path):
        print(f"❌ Erro: Arquivo {csv_path} não encontrado!")
        return
    
    # Ler CSV
    print(f"📖 Lendo CSV ({os.path.getsize(csv_path) / (1024*1024):.2f} MB)...")
    df = pd.read_csv(csv_path)
    
    print(f"✅ CSV carregado: {len(df):,} registros")
    print(f"📊 Colunas: {list(df.columns)}")
    
    # Converter coluna de data para datetime
    if 'data_criacao_transacao' in df.columns:
        print("📅 Convertendo coluna data para datetime...")
        df['data_criacao_transacao'] = pd.to_datetime(df['data_criacao_transacao'], errors='coerce')
    
    # Salvar como Parquet com compressão gzip
    print("💾 Salvando como Parquet comprimido...")
    df.to_parquet(
        parquet_path,
        engine='pyarrow',
        compression='gzip',
        index=False
    )
    
    # Estatísticas
    parquet_size = os.path.getsize(parquet_path) / (1024*1024)
    csv_size = os.path.getsize(csv_path) / (1024*1024)
    reducao = ((csv_size - parquet_size) / csv_size) * 100
    
    print("\n" + "="*60)
    print("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print(f"📊 Registros: {len(df):,}")
    print(f"📁 Tamanho CSV: {csv_size:.2f} MB")
    print(f"🗜️  Tamanho Parquet: {parquet_size:.2f} MB")
    print(f"📉 Redução: {reducao:.1f}%")
    print(f"💾 Arquivo criado: {parquet_path}")
    print("="*60)
    
    # Testar leitura
    print("\n🧪 Testando leitura do Parquet...")
    test_df = pd.read_parquet(parquet_path)
    print(f"✅ Leitura OK: {len(test_df):,} registros")
    print(test_df.head())
    
    print("\n✅ Arquivo Parquet pronto para uso!")
    print("💡 Agora atualize o dashboard.py para usar Parquet")

if __name__ == "__main__":
    criar_parquet()
