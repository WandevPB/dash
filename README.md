# 📊 Dashboard Regional - Análise de Movimentação de Estoque

Dashboard interativo desenvolvido em Streamlit para análise de movimentação de inventário regional de múltiplas localidades no Ceará.

## 🎯 Funcionalidades

- **📈 Ranking de Localidades** por volume de transações
- **📊 Análise Mensal Detalhada** com múltiplas linhas por localidade
- **🧵 Evolução de Cabos (metros)** ao longo dos meses
- **📦 Evolução de Itens Serializados** (contagem única)
- **📊 Evolução de Itens Quantitativos** (contagem de aparições)
- **🧵 Top Cabos** - Ranking dos cabos mais movimentados
- **🎨 Temas Claro e Escuro**
- **🔍 Filtros Dinâmicos** por localidade

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.13+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/WandevPB/dash.git
cd dash

# Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
dash/
├── dashboard.py              # Aplicação principal
├── mapping.py               # Normalização de nomes de localidades
├── style.css                # Estilos customizados (tema claro)
├── requirements.txt         # Dependências Python
├── dados/
│   └── dados_consolidados_2025.csv  # Dados consolidados (otimizado)
└── README.md
```

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework web para aplicações de dados
- **Pandas** - Manipulação e análise de dados
- **PyEcharts** - Visualizações interativas com animações
- **Python 3.13** - Linguagem de programação

## 📊 Dados

O dashboard utiliza dados consolidados de movimentação de estoque de 16 localidades no período de **janeiro a setembro de 2025**, incluindo:

- **1.7+ milhões** de registros de transações
- **48,854** transações únicas
- **5,125** subcategorias de produtos
- **35** categorias principais
- **16** localidades normalizadas

## 🎨 Características Visuais

- Tema laranja (#F97316) personalizado
- Gráficos animados e interativos
- Legenda com scroll para múltiplas localidades
- Tooltips informativos com z-index otimizado
- Layout responsivo de 3 colunas
- KPIs com gradiente animado

## 🔧 Otimizações Implementadas

- ✅ Cache de dados com `@st.cache_data`
- ✅ Carregamento seletivo de colunas
- ✅ Arquivo consolidado (redução de 68% no tamanho)
- ✅ Pré-filtro de dados de 2025
- ✅ Processamento otimizado com pandas

## 📝 Licença

Este projeto é de uso interno.

## 👨‍💻 Desenvolvedor

Wanderson Gonçalves

---

⭐ Se você achou útil, deixe uma estrela no repositório!
