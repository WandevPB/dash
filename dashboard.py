import streamlit as st
import pandas as pd
import re
from mapping import normalizar_deposito
from streamlit_echarts import st_echarts

# ===== CONFIGURAÇÃO GERAL =====
st.set_page_config(page_title="📊 Dashboard Regional", page_icon="📊", layout="wide")

# ===== FONT AWESOME =====
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-CmZcdBGvlvcdwVYGoLqJip/Yy04NVlSV6J8I9fKUrS3vhFTe9on1J9iBIr3AaIUdYrh+wHV1G9eZwxDfAtYh1g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<script>
// Força tooltip do ECharts sempre visível
document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && node.style && node.style.position === 'absolute') {
                    node.style.zIndex = '9999999';
                    node.style.pointerEvents = 'none';
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});
</script>
""", unsafe_allow_html=True)

# ===== SELETOR DE TEMA =====
st.sidebar.header("🎨 Tema")
tema = st.sidebar.radio("Escolha o tema:", ["☀️ Claro", "🌙 Escuro"], horizontal=True, label_visibility="collapsed")
tema_escuro = tema == "🌙 Escuro"

# ===== CSS CUSTOM =====
if tema_escuro:
    css_tema = """
    :root {
      --primary: #F97316;
      --bg: #1a1a1a;
      --card: #2d2d2d;
      --border: #404040;
      --text: #e5e5e5;
      --text-secondary: #a3a3a3;
      --radius: 8px;
      --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.07);
    }
    
    body {
      background-color: var(--bg);
      color: var(--text);
    }
    
    .block-container {
      padding-top: 2rem;
      max-width: 1400px;
    }
    
    .navbar {
      background: var(--card);
      border-radius: var(--radius);
      padding: 12px 20px;
      margin-bottom: 24px;
      box-shadow: var(--shadow);
    }
    
    .navbar .title {
      color: var(--primary);
      font-weight: 700;
      font-size: 1.5rem;
    }
    
    .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow);
      transition: all 0.3s ease;
    }
    
    .panel-title {
      color: var(--primary);
      font-weight: 600;
      border-left: 4px solid var(--primary);
      padding-left: 12px;
      margin-bottom: 20px;
      font-size: 1.2rem;
    }
    
    .kpi-card {
      background: linear-gradient(135deg, #F97316, #F59E0B);
      color: white;
      padding: 20px;
      border-radius: var(--radius);
      min-height: 130px;
      box-shadow: 0 10px 15px -3px rgba(249, 115, 22, 0.2), 0 4px 6px -4px rgba(249, 115, 22, 0.1);
      transition: all 0.3s ease-in-out;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    
    .kpi-card:hover {
      transform: translateY(-6px);
      box-shadow: 0 20px 25px -5px rgba(249, 115, 22, 0.25), 0 8px 10px -6px rgba(249, 115, 22, 0.15);
    }
    
    .kpi-icon { font-size: 2rem; margin-bottom: 8px; }
    .kpi-title { font-size: 0.8rem; text-transform: uppercase; font-weight: 600; opacity: 0.9; }
    .kpi-number { font-size: 2.2rem; font-weight: 700; line-height: 1.1; }
    
    /* Ajustes globais para modo escuro */
    .stApp {
      background-color: var(--bg);
    }
    
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6 {
      color: var(--text);
    }
    
    /* Tabelas em modo escuro */
    .stDataFrame {
      background-color: var(--card);
      color: var(--text);
    }
    
    /* Força tooltips do ECharts sempre visíveis */
    div[class*="echarts"] {
      position: relative !important;
      z-index: 1 !important;
      overflow: visible !important;
    }
    
    div[class*="tooltip"], .echarts-tooltip, div[style*="position: absolute"] {
      z-index: 9999999 !important;
      pointer-events: none !important;
    }
    
    /* Container do streamlit-echarts - todos os níveis */
    .stEcharts, .stEcharts > div, .stEcharts > div > div, .stEcharts > div > div > div {
      position: relative !important;
      overflow: visible !important;
      z-index: auto !important;
    }
    
    /* Força overflow visível nos painéis e colunas */
    .panel, [data-testid="column"], [data-testid="stHorizontalBlock"] {
      overflow: visible !important;
      position: relative !important;
      z-index: auto !important;
    }
    
    /* Força overlay do tooltip - máxima prioridade */
    canvas {
      z-index: 1 !important;
      position: relative !important;
    }
    
    /* Garante que elementos gráficos fiquem abaixo do tooltip */
    svg, canvas, .echarts-layer {
      z-index: 1 !important;
    }
    
    /* Tooltip sempre no topo - captura todos os elementos de posição absoluta no body */
    body > div[style*="position: absolute"],
    body > div[style*="position:absolute"],
    div[style*="pointer-events: none"][style*="position: absolute"] {
      z-index: 9999999 !important;
    }
    
    /* Remove qualquer z-index que possa interferir */
    .block-container {
      z-index: auto !important;
    }
    """
else:
    with open("style.css", "r", encoding="utf-8") as f:
        css_tema = f.read()

st.markdown(f"<style>{css_tema}</style>", unsafe_allow_html=True)

# ===== FUNÇÕES =====
def detect_sep(path):
    with open(path, "r", encoding="utf-8") as f:
        head = f.read(2048)
    return ";" if head.count(";") > head.count(",") else ","

@st.cache_data
def load_csv(file):
    if hasattr(file, "read"):
        file.seek(0)
        return pd.read_csv(file, sep=None, engine="python")
    sep = detect_sep(file)
    return pd.read_csv(file, sep=sep, low_memory=False)

@st.cache_data
def load_all_csvs_from_folder(pasta="dados"):
    """Carrega dados do arquivo Parquet otimizado"""
    import pandas as pd
    import os
    
    parquet_path = os.path.join(pasta, "inventario.parquet")
    
    if not os.path.exists(parquet_path):
        st.error(f"❌ Arquivo Parquet não encontrado: {parquet_path}")
        st.info("Execute: python criar_parquet.py")
        return pd.DataFrame()
    
    # Carregar arquivo Parquet (96.5% menor que CSV, leitura 10-50x mais rápida)
    df = pd.read_parquet(parquet_path)
    
    return df

@st.cache_data
def enrich(df):
    """Processa e enriquece os dados - COM CACHE"""
    df.columns = [c.lower().strip() for c in df.columns]
    df["data_criacao_transacao"] = pd.to_datetime(df["data_criacao_transacao"], errors="coerce", dayfirst=True)
    
    # Filtrar apenas dados de 2025: 01/01/2025 até 30/09/2025
    data_inicio = pd.Timestamp("2025-01-01")
    data_fim = pd.Timestamp("2025-09-30")
    df = df[(df["data_criacao_transacao"] >= data_inicio) & (df["data_criacao_transacao"] <= data_fim)]
    
    # Criar coluna mes com nome do mês
    df["mes_num"] = df["data_criacao_transacao"].dt.month
    meses_map = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    df["mes"] = df["mes_num"].map(meses_map)
    
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0)
    df["quantidade"] = df["quantidade"].replace(0, 1)
    df["localidade"] = df["deposito_origem_nome"].apply(normalizar_deposito)
    
    # Verificar se tem número de série (verificar se coluna existe e se tem valor)
    if "numero_serie" in df.columns:
        df["tem_serie"] = df["numero_serie"].astype(str).str.strip().ne("") & df["numero_serie"].notna()
    else:
        df["tem_serie"] = False
    
    # Extrair código SAP: se começar com número = 10 primeiros dígitos, senão = subcategoria completa
    def extrair_codigo_sap(subcategoria):
        subcat_str = str(subcategoria).strip()
        if subcat_str and subcat_str[0].isdigit():
            return subcat_str[:10]  # Código SAP: 10 primeiros dígitos
        else:
            return subcat_str  # Subcategoria completa se começar com letra
    
    df["codigo_sap"] = df["subcategoria"].apply(extrair_codigo_sap)
    
    # Identificar cabos pela categoria (CABO ou CABO ELETRICO)
    df["is_cabo"] = df["categoria"].astype(str).str.upper().str.strip().isin(["CABO", "CABO ELETRICO"])
    
    return df

# Funções para gráficos ECharts
def criar_grafico_linha_echarts(df_data, tema_escuro=False):
    """Cria gráfico de linha com ECharts - Evolução Mensal"""
    localidades = df_data["localidade"].unique().tolist()
    meses = sorted(df_data["mes"].unique().tolist())
    
    cores = ['#F97316', '#FB923C', '#EA580C', '#F59E0B', '#FCD34D', 
             '#DC2626', '#EF4444', '#F87171', '#FB7185', '#FDBA74']
    
    series_data = []
    for idx, loc in enumerate(localidades):
        data_loc = df_data[df_data["localidade"] == loc]
        valores = []
        for mes in meses:
            val = data_loc[data_loc["mes"] == mes]["quantidade"].sum()
            valores.append(int(val) if val > 0 else 0)
        
        series_data.append({
            "name": loc,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "lineStyle": {"width": 3},
            "areaStyle": {"opacity": 0.3},
            "emphasis": {"focus": "series"},
            "data": valores,
            "itemStyle": {"color": cores[idx % len(cores)]}
        })
    
    option = {
        "title": {
            "text": "📈 Evolução de SKUs Únicos por Localidade",
            "left": "center",
            "textStyle": {"color": "#F97316", "fontSize": 20, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
            "backgroundColor": "rgba(255,255,255,0.95)",
            "borderColor": "#F97316",
            "borderWidth": 2,
            "textStyle": {"color": "#333"}
        },
        "legend": {
            "bottom": 10,
            "data": localidades,
            "textStyle": {"color": "#666" if not tema_escuro else "#e5e5e5"}
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "15%", "top": "15%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": meses,
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5"}
        },
        "yAxis": {
            "type": "value",
            "name": "Quantidade",
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5"},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.2}}
        },
        "series": series_data,
        "animationDuration": 1000,
        "animationEasing": "cubicOut"
    }
    return option

def criar_grafico_linha_simples(df_data, titulo, tema_escuro=False, y_label="Quantidade"):
    """Cria gráfico de linha simples mensal para métricas específicas"""
    # Mapear nomes de meses para abreviações
    meses_map = {
        "Janeiro": "JAN", "Fevereiro": "FEV", "Março": "MAR", "Abril": "ABR",
        "Maio": "MAI", "Junho": "JUN", "Julho": "JUL", "Agosto": "AGO",
        "Setembro": "SET", "Outubro": "OUT", "Novembro": "NOV", "Dezembro": "DEZ"
    }
    
    # Ordenar meses corretamente
    meses_ordem = list(meses_map.keys())
    df_sorted = df_data.copy()
    df_sorted["mes_ordem"] = df_sorted["mes"].apply(lambda x: meses_ordem.index(x) if x in meses_ordem else 999)
    df_sorted = df_sorted.sort_values("mes_ordem")
    
    meses_abrev = [meses_map.get(m, m) for m in df_sorted["mes"]]
    valores = df_sorted["valor"].tolist()
    
    option = {
        "title": {
            "text": titulo,
            "left": "center",
            "textStyle": {"color": "#F97316", "fontSize": 16, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": "rgba(255,255,255,0.95)",
            "borderColor": "#F97316",
            "borderWidth": 2,
            "textStyle": {"color": "#333"}
        },
        "grid": {"left": "15%", "right": "10%", "bottom": "15%", "top": "20%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": meses_abrev,
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5", "fontSize": 10}
        },
        "yAxis": {
            "type": "value",
            "name": y_label,
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {
                "color": "#666" if not tema_escuro else "#e5e5e5", 
                "fontSize": 10
            },
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.2}}
        },
        "series": [{
            "type": "line",
            "data": valores,
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "lineStyle": {"width": 3, "color": "#F97316"},
            "itemStyle": {"color": "#F97316"},
            "areaStyle": {"opacity": 0.2, "color": "#F97316"},
            "label": {
                "show": True,
                "position": "top",
                "color": "#F97316",
                "fontSize": 10,
                "fontWeight": "bold"
            }
        }],
        "animationDuration": 1000,
        "animationEasing": "cubicOut"
    }
    return option

def criar_grafico_linha_multi_localidade(df_data, titulo, tema_escuro=False, y_label="Quantidade"):
    """Cria gráfico de linha com múltiplas localidades"""
    # Mapear nomes de meses para abreviações
    meses_map = {
        "Janeiro": "JAN", "Fevereiro": "FEV", "Março": "MAR", "Abril": "ABR",
        "Maio": "MAI", "Junho": "JUN", "Julho": "JUL", "Agosto": "AGO",
        "Setembro": "SET", "Outubro": "OUT", "Novembro": "NOV", "Dezembro": "DEZ"
    }
    
    cores = ['#F97316', '#FB923C', '#EA580C', '#F59E0B', '#FCD34D', 
             '#DC2626', '#EF4444', '#F87171', '#FB7185', '#FDBA74',
             '#FCA5A5', '#FBBF24', '#FDE68A', '#FED7AA', '#FEF3C7']
    
    # Pegar localidades e meses únicos
    localidades = sorted(df_data["localidade"].unique())
    meses_ordem = list(meses_map.keys())
    meses = sorted(df_data["mes"].unique(), key=lambda x: meses_ordem.index(x) if x in meses_ordem else 999)
    meses_abrev = [meses_map.get(m, m) for m in meses]
    
    series_data = []
    for idx, loc in enumerate(localidades):
        df_loc = df_data[df_data["localidade"] == loc]
        valores = []
        for mes in meses:
            val = df_loc[df_loc["mes"] == mes]["valor"].sum()
            valores.append(int(val) if val > 0 else 0)
        
        series_data.append({
            "name": loc,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 4,
            "lineStyle": {"width": 2},
            "emphasis": {"focus": "series"},
            "data": valores,
            "itemStyle": {"color": cores[idx % len(cores)]},
            "z": 1  # z-index baixo para linhas
        })
    
    option = {
        "title": {
            "text": titulo,
            "left": "center",
            "top": "2%",
            "textStyle": {
                "color": "#F97316",
                "fontSize": 16,
                "fontWeight": "bold"
            }
        },
        "tooltip": {
            "trigger": "axis",
            "backgroundColor": "rgba(255,255,255,0.98)",
            "borderColor": "#F97316",
            "borderWidth": 2,
            "textStyle": {"color": "#333", "fontSize": 11},
            "confine": True,
            "extraCssText": "z-index: 9999999 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15); pointer-events: none;",
            "axisPointer": {
                "type": "line",
                "lineStyle": {"color": "#F97316", "width": 1, "type": "dashed"},
                "z": 9999998
            }
        },
        "legend": {
            "type": "scroll",
            "bottom": 0,
            "left": "center",
            "orient": "horizontal",
            "data": localidades,
            "textStyle": {"color": "#666" if not tema_escuro else "#e5e5e5", "fontSize": 8},
            "pageIconSize": 10,
            "pageTextStyle": {"fontSize": 8}
        },
        "grid": {"left": "8%", "right": "5%", "bottom": "22%", "top": "15%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": meses_abrev,
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5", "fontSize": 9}
        },
        "yAxis": {
            "type": "value",
            "name": y_label,
            "nameTextStyle": {"fontSize": 9},
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5", "fontSize": 9},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.2}}
        },
        "series": series_data,
        "animationDuration": 1000,
        "animationEasing": "cubicOut"
    }
    return option



def criar_grafico_barras_echarts(df_data, tema_escuro=False):
    """Cria gráfico de barras horizontais com ECharts - Todos os Cabos"""
    top_n = 15
    df_sorted = df_data.head(top_n)
    
    cores = ['#F97316', '#FB923C', '#FDBA74', '#F59E0B', '#FCD34D',
             '#EA580C', '#FB7185', '#EF4444', '#DC2626', '#FBBF24',
             '#FCA5A5', '#F87171', '#FDE68A', '#FEF3C7', '#FED7AA']
    
    categorias = df_sorted["subcategoria"].tolist()
    valores = df_sorted["quantidade"].tolist()
    colors_list = [cores[i % len(cores)] for i in range(len(categorias))]
    
    data_with_style = []
    for i, val in enumerate(valores):
        data_with_style.append({
            "value": val,
            "itemStyle": {"color": colors_list[i]}
        })
    
    option = {
        "title": {
            "text": "🧵 Top Cabos",
            "left": "center",
            "textStyle": {"color": "#F97316", "fontSize": 20, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "backgroundColor": "rgba(255,255,255,0.95)",
            "borderColor": "#F97316",
            "borderWidth": 2,
            "textStyle": {"color": "#333"}
        },
        "grid": {"left": "30%", "right": "10%", "top": "15%", "bottom": "5%"},
        "xAxis": {
            "type": "value",
            "name": "Metros",
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5"},
            "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.2}}
        },
        "yAxis": {
            "type": "category",
            "data": categorias,
            "axisLine": {"lineStyle": {"color": "#F97316"}},
            "axisLabel": {"color": "#666" if not tema_escuro else "#e5e5e5", "fontSize": 11}
        },
        "series": [{
            "type": "bar",
            "data": data_with_style,
            "itemStyle": {"borderRadius": [0, 8, 8, 0]},
            "label": {
                "show": True,
                "position": "right",
                "formatter": "{c}m",
                "color": "#F97316",
                "fontWeight": "bold"
            },
            "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(249,115,22,0.5)"}}
        }],
        "animationDuration": 1000,
        "animationEasing": "elasticOut"
    }
    return option

def criar_grafico_pizza_echarts(df_data, tema_escuro=False):
    """Cria gráfico de pizza com ECharts - Participação por Localidade"""
    cores = ['#F97316', '#FB923C', '#FDBA74', '#EA580C', '#F59E0B',
             '#FCD34D', '#DC2626', '#EF4444', '#F87171', '#FB7185',
             '#FBBF24', '#FDE68A', '#FEF3C7', '#FED7AA', '#FCA5A5']
    
    data_pizza = []
    for idx, row in df_data.iterrows():
        data_pizza.append({
            "value": int(row["quantidade"]),
            "name": row["localidade"],
            "itemStyle": {"color": cores[idx % len(cores)]}
        })
    
    option = {
        "title": {
            "text": "🏢 Dados de Transações",
            "left": "center",
            "textStyle": {"color": "#F97316", "fontSize": 20, "fontWeight": "bold"}
        },
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "rgba(255,255,255,0.95)",
            "borderColor": "#F97316",
            "borderWidth": 2,
            "textStyle": {"color": "#333"}
        },
        "legend": {
            "orient": "vertical",
            "right": "5%",
            "top": "center",
            "textStyle": {"color": "#666" if not tema_escuro else "#e5e5e5"}
        },
        "series": [{
            "type": "pie",
            "radius": ["40%", "70%"],
            "center": ["40%", "50%"],
            "data": data_pizza,
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 20,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(249,115,22,0.5)"
                }
            },
            "label": {
                "show": True,
                "formatter": "{b}\n{d}%",
                "color": "#666" if not tema_escuro else "#e5e5e5"
            },
            "labelLine": {"show": True, "smooth": True}
        }],
        "animationType": "scale",
        "animationEasing": "elasticOut",
        "animationDuration": 1000
    }
    return option

# ===== CARREGAR DADOS =====
st.sidebar.header("📁 Dados")
uploaded = st.sidebar.file_uploader("Envie CSV", type=["csv"])
if uploaded:
    df = load_csv(uploaded)
    df = enrich(df)
else:
    df = load_all_csvs_from_folder("dados")
    if not df.empty:
        df = enrich(df)
    else:
        st.error("❌ Nenhum dado disponível. Adicione arquivos CSV na pasta 'dados/' ou faça upload.")
        st.stop()

# ===== NAVBAR =====
st.markdown('<div class="navbar">', unsafe_allow_html=True)
st.markdown('<div class="title">📊 Dashboard Regional</div>', unsafe_allow_html=True)
meses = sorted(df["mes"].unique())
localidades = sorted(df["localidade"].dropna().unique())
col1, col2 = st.columns([1, 3])
mes_sel = col1.selectbox("Mês", ["Todos"] + meses, label_visibility="collapsed")
loc_sel = col2.multiselect("Localidade", localidades, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ===== FILTROS =====
df_filt = df.copy()
if mes_sel != "Todos":
    df_filt = df_filt[df_filt["mes"] == mes_sel]
if loc_sel:
    df_filt = df_filt[df_filt["localidade"].isin(loc_sel)]

# ===== KPIs GERAIS (Respeitam os filtros) =====
# Total SKUs únicos movimentados (exceto cabos que somam quantidade)
total_skus = df_filt["codigo_sap"].nunique()
total_series = df_filt.loc[df_filt["tem_serie"], "numero_serie"].nunique()
total_cabos = df_filt.loc[df_filt["is_cabo"], "quantidade"].sum()
# Localidade com maior volume de transações
local_top = df_filt.groupby("localidade")["transacao_id"].nunique().idxmax() if not df_filt.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon"><i class="fa-solid fa-cubes"></i></div>
      <div class="kpi-title">SKUs Únicos Movimentados</div>
      <div class="kpi-number">{total_skus:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon"><i class="fa-solid fa-barcode"></i></div>
      <div class="kpi-title">ITENS SERIALIZADOS</div>
      <div class="kpi-number">{total_series:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon"><i class="fa-solid fa-ethernet"></i></div>
      <div class="kpi-title">Cabos (m)</div>
      <div class="kpi-number">{total_cabos:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon"><i class="fa-solid fa-trophy"></i></div>
      <div class="kpi-title">Localidade com mais movimentação</div>
      <div class="kpi-number" style="font-size: 1.3rem;">{local_top}</div>
    </div>
    """, unsafe_allow_html=True)

# ===== GRÁFICOS =====

# --- Evolução Mensal (3 Gráficos) ---
# Determinar localidades sendo visualizadas
localidades_visualizadas = loc_sel if loc_sel else sorted(df_filt["localidade"].unique())
loc_texto = ", ".join(localidades_visualizadas) if len(localidades_visualizadas) <= 3 else f"{len(localidades_visualizadas)} localidades"

st.markdown(f'<h2 style="color: #F97316; margin: 30px 0 20px 0; font-weight: 700; border-bottom: 3px solid #F97316; padding-bottom: 10px;">📊 Análise Mensal Detalhada - {loc_texto}</h2>', unsafe_allow_html=True)

col_g1, col_g2, col_g3 = st.columns(3)

# Preparar dados filtrados para análise mensal (com otimização)
df_evo = df_filt.copy()

# Pré-calcular filtros para evitar recalcular 3 vezes
df_cabos_filter = df_evo[df_evo["is_cabo"]]
df_series_filter = df_evo[df_evo["tem_serie"]]
df_quant_filter = df_evo[(df_evo["tem_serie"] == False) & (~df_evo["is_cabo"])]

# Gráfico 1: Cabos por mês POR LOCALIDADE
with col_g1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if not df_cabos_filter.empty:
        df_cabos_mes = df_cabos_filter.groupby(["mes", "localidade"])["quantidade"].sum().reset_index()
        df_cabos_mes.columns = ["mes", "localidade", "valor"]
        
        option_cabos = criar_grafico_linha_multi_localidade(df_cabos_mes, "🧵 Cabos (m) por Mês", tema_escuro, "Metros")
        st_echarts(options=option_cabos, height="450px", key="grafico_cabos")
    else:
        st.info("Sem dados de cabos")
    st.markdown('</div>', unsafe_allow_html=True)

# Gráfico 2: Itens Serializados por mês POR LOCALIDADE
with col_g2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if not df_series_filter.empty:
        df_series_mes = df_series_filter.groupby(["mes", "localidade"])["numero_serie"].nunique().reset_index()
        df_series_mes.columns = ["mes", "localidade", "valor"]
        
        option_series = criar_grafico_linha_multi_localidade(df_series_mes, "📦 Itens Serializados por Mês", tema_escuro, "Qtd")
        st_echarts(options=option_series, height="450px", key="grafico_series")
    else:
        st.info("Sem dados de séries")
    st.markdown('</div>', unsafe_allow_html=True)

# Gráfico 3: Itens Quantitativos por mês POR LOCALIDADE
with col_g3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if len(df_quant_filter) > 0:
        # Contar aparições por mês e localidade
        df_quant_mes = df_quant_filter.groupby(["mes", "localidade"]).size().reset_index()
        df_quant_mes.columns = ["mes", "localidade", "valor"]
        
        option_quant = criar_grafico_linha_multi_localidade(df_quant_mes, "📊 Itens Quantitativos por Mês", tema_escuro, "Qtd")
        st_echarts(options=option_quant, height="450px", key="grafico_quant")
    else:
        st.info("Sem dados quantitativos")
    st.markdown('</div>', unsafe_allow_html=True)


# --- Cabos (Todos os tipos) ---
st.markdown('<div class="panel">', unsafe_allow_html=True)
cabos_viz = df_filt[df_filt["is_cabo"]]
if not cabos_viz.empty:
    # Agrupar pelo código SAP e pegar uma subcategoria como nome
    rank = cabos_viz.groupby("codigo_sap").agg({
        "quantidade": "sum",
        "subcategoria": "first"  # Pega o primeiro nome encontrado para o código SAP
    }).reset_index().sort_values("quantidade", ascending=False)
    option_barras = criar_grafico_barras_echarts(rank, tema_escuro)
    st_echarts(options=option_barras, height="600px")
else:
    st.info("Sem dados de cabos para os filtros atuais.")
st.markdown('</div>', unsafe_allow_html=True)

# --- Localidades ---
st.markdown('<div class="panel">', unsafe_allow_html=True)
share = df_filt.groupby("localidade").agg({
    "transacao_id": "nunique",  # Ranking por volume de transações
    "codigo_sap": "nunique"
}).reset_index()
share.rename(columns={"transacao_id": "transacoes", "codigo_sap": "skus_unicos"}, inplace=True)

if not share.empty:
    # Calcular percentuais baseado em volume de transações
    share["percentual"] = (share["transacoes"] / share["transacoes"].sum() * 100)
    
    # Preparar dados para o gráfico (usar transações como quantidade)
    share_chart = share.copy()
    share_chart["quantidade"] = share_chart["transacoes"]
    option_pizza = criar_grafico_pizza_echarts(share_chart, tema_escuro)
    st_echarts(options=option_pizza, height="500px")
    
    # Tabela de resumo
    st.markdown('<div style="margin-top: 24px;"><h3 style="color: #F97316; font-size: 1rem; font-weight: 600; margin-bottom: 12px; border-left: 3px solid #F97316; padding-left: 8px;">📊 Resumo Detalhado</h3></div>', unsafe_allow_html=True)
    
    share_display = share[["localidade", "transacoes", "skus_unicos", "percentual"]].copy()
    share_display = share_display.sort_values("transacoes", ascending=False)  # Ordenar por transações
    
    share_display["transacoes_fmt"] = share_display["transacoes"].apply(lambda x: f"{x:,.0f}")
    share_display["skus_fmt"] = share_display["skus_unicos"].apply(lambda x: f"{x:,.0f}")
    share_display["percentual_fmt"] = share_display["percentual"].apply(
        lambda x: "< 0.1%" if 0 < x < 0.1 else f"{x:.1f}%"
    )
    
    display_df = share_display[["localidade", "transacoes_fmt", "skus_fmt", "percentual_fmt"]].copy()
    display_df.columns = ["🏢 Localidade", "📝 Transações", "📦 SKUs Únicos", "📊 Percentual"]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "🏢 Localidade": st.column_config.TextColumn(width="medium"),
            "📝 Transações": st.column_config.TextColumn(width="small"),
            "📦 SKUs Únicos": st.column_config.TextColumn(width="medium"),
            "📊 Percentual": st.column_config.TextColumn(width="small")
        }
    )
else:
    st.info("Sem dados para exibir.")
st.markdown('</div>', unsafe_allow_html=True)

# --- Serializados ---
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<h3 style="color: #F97316; font-size: 1.2rem; font-weight: 600; margin-bottom: 16px;">📦 Itens Serializados</h3>', unsafe_allow_html=True)
series_viz = df_filt[df_filt["tem_serie"]]
if not series_viz.empty:
    st.metric("Total de Séries Únicas", f"{series_viz['numero_serie'].nunique():,}")
    # Agrupar por código SAP ao invés de subcategoria completa
    top_series = series_viz.groupby("codigo_sap").agg({
        "numero_serie": "nunique",
        "subcategoria": "first"  # Nome do item
    }).reset_index()
    top_series.columns = ["Código SAP", "Qtd Séries", "Item"]
    top_series = top_series.sort_values("Qtd Séries", ascending=False).head(10)
    # Reordenar colunas para melhor visualização
    top_series = top_series[["Código SAP", "Item", "Qtd Séries"]]
    st.dataframe(top_series, use_container_width=True, hide_index=True)
else:
    st.info("Sem itens serializados para os filtros atuais.")
st.markdown('</div>', unsafe_allow_html=True)
