"""
Script para converter CSV consolidado em banco de dados SQLite
Muito mais rápido e eficiente para o Streamlit Cloud
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

def criar_database():
    """Converte o CSV consolidado em banco SQLite otimizado"""
    
    print("🔄 Iniciando conversão para SQLite...")
    
    # Caminhos
    csv_path = 'dados/dados_consolidados_2025.csv'
    db_path = 'dados/inventario.db'
    
    # Verificar se CSV existe
    if not os.path.exists(csv_path):
        print(f"❌ Erro: Arquivo {csv_path} não encontrado!")
        return
    
    # Ler CSV
    print(f"📖 Lendo CSV ({os.path.getsize(csv_path) / (1024*1024):.2f} MB)...")
    df = pd.read_csv(csv_path)
    
    print(f"✅ CSV carregado: {len(df):,} registros")
    print(f"📊 Colunas: {list(df.columns)}")
    
    # Converter coluna de data para datetime se existir
    if 'Data' in df.columns:
        print("📅 Convertendo coluna Data para datetime...")
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
    # Criar conexão SQLite
    print("🗄️  Criando banco de dados SQLite...")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("   (Removendo banco antigo)")
    
    conn = sqlite3.connect(db_path)
    
    # Salvar DataFrame no SQLite
    print("💾 Salvando dados no banco...")
    df.to_sql('inventario', conn, if_exists='replace', index=False, chunksize=10000)
    
    # Criar índices para consultas rápidas
    print("⚡ Criando índices para acelerar consultas...")
    cursor = conn.cursor()
    
    # Índices nas colunas mais usadas
    if 'Local' in df.columns:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_local ON inventario(Local)')
        print("   ✓ Índice em 'Local'")
    
    if 'Data' in df.columns:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_data ON inventario(Data)')
        print("   ✓ Índice em 'Data'")
    
    if 'Produto' in df.columns:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_produto ON inventario(Produto)')
        print("   ✓ Índice em 'Produto'")
    
    # Índice composto para consultas por local e data
    if 'Local' in df.columns and 'Data' in df.columns:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_local_data ON inventario(Local, Data)')
        print("   ✓ Índice composto 'Local + Data'")
    
    conn.commit()
    
    # Estatísticas
    db_size = os.path.getsize(db_path) / (1024*1024)
    csv_size = os.path.getsize(csv_path) / (1024*1024)
    reducao = ((csv_size - db_size) / csv_size) * 100
    
    print("\n" + "="*60)
    print("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print(f"📊 Registros no banco: {len(df):,}")
    print(f"📁 Tamanho CSV: {csv_size:.2f} MB")
    print(f"🗄️  Tamanho SQLite: {db_size:.2f} MB")
    print(f"📉 Redução: {reducao:.1f}%")
    print(f"💾 Arquivo criado: {db_path}")
    print("="*60)
    
    # Testar consulta
    print("\n🧪 Testando consulta no banco...")
    test_df = pd.read_sql_query("SELECT * FROM inventario LIMIT 5", conn)
    print(test_df)
    
    conn.close()
    
    print("\n✅ Banco de dados pronto para uso!")
    print("💡 Agora atualize o dashboard.py para usar SQLite ao invés de CSV")

if __name__ == "__main__":
    criar_database()
