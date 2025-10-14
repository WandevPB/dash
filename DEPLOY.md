# 🚀 Guia de Deploy - GitHub + Streamlit Cloud

## 📋 Checklist Pré-Deploy

- [x] Dados consolidados (207 MB)
- [x] .gitignore criado
- [x] README.md criado
- [x] requirements.txt atualizado
- [ ] Push para GitHub
- [ ] Deploy no Streamlit Cloud

## 1️⃣ Configurar Git e Fazer Push

Execute os comandos abaixo no terminal:

```bash
# Navegue até a pasta do projeto
cd c:\Users\wanderson.goncalves_\Desktop\DashRegional

# Inicialize o Git (se ainda não foi feito)
git init

# Configure o repositório remoto
git remote add origin https://github.com/WandevPB/dash.git

# Ou, se já existe, atualize a URL:
git remote set-url origin https://github.com/WandevPB/dash.git

# Adicione todos os arquivos (exceto os do .gitignore)
git add .

# Faça o commit
git commit -m "Dashboard Regional - Análise de Movimentação de Estoque"

# Configure a branch principal
git branch -M main

# Faça o push
git push -u origin main
```

**⚠️ IMPORTANTE:** Se o arquivo `dados_consolidados_2025.csv` (207 MB) for maior que 100 MB, o GitHub vai bloquear. Veja soluções abaixo.

## ⚠️ Se o Arquivo for Maior que 100 MB

### Solução 1: Git LFS (Large File Storage)

```bash
# Instale o Git LFS (se não tiver)
# Download: https://git-lfs.github.com/

# Configure o Git LFS
git lfs install

# Rastreie o arquivo grande
git lfs track "dados/dados_consolidados_2025.csv"

# Adicione o .gitattributes
git add .gitattributes

# Adicione e faça commit normalmente
git add dados/dados_consolidados_2025.csv
git commit -m "Adicionar dados consolidados via LFS"
git push
```

### Solução 2: Comprimir o Arquivo

```bash
# Comprimir o CSV (pode reduzir 80-90%)
# Execute no Python:
python -c "import pandas as pd; df = pd.read_csv('dados/dados_consolidados_2025.csv'); df.to_parquet('dados/dados_consolidados_2025.parquet', compression='gzip')"

# Depois atualize o dashboard.py para ler .parquet em vez de .csv
```

## 2️⃣ Deploy no Streamlit Community Cloud

### Passos:

1. **Acesse:** https://streamlit.io/cloud
2. **Faça login** com sua conta GitHub
3. **Clique em "New app"**
4. **Preencha:**
   - Repository: `WandevPB/dash`
   - Branch: `main`
   - Main file path: `dashboard.py`
5. **Clique em "Deploy!"**

### ⏱️ Tempo de Deploy:
- Primeira vez: 5-10 minutos
- Atualizações: 2-3 minutos

### 🔗 URL Final:
Seu dashboard ficará disponível em:
```
https://[seu-app-name].streamlit.app
```

## 3️⃣ Configurações Opcionais no Streamlit Cloud

Após o deploy, você pode:

1. **Customizar URL** (se disponível)
2. **Adicionar secrets** (se houver dados sensíveis)
3. **Configurar analytics**
4. **Ativar senha** (recursos do plano pago)

## 🔄 Atualizações Futuras

Para atualizar o dashboard após o deploy:

```bash
# Faça suas alterações
# Depois:

git add .
git commit -m "Descrição das mudanças"
git push

# O Streamlit Cloud detecta automaticamente e redeploy!
```

## 📊 Monitoramento

- **Logs:** Disponíveis no painel do Streamlit Cloud
- **Métricas:** Views, tempo de carregamento, etc.
- **Erros:** Notificações por email (se configurado)

## ⚠️ Limites do Plano Gratuito

- **1 GB de RAM** por app
- **1 CPU** compartilhado
- **Sleep após 7 dias** de inatividade
- **Sem senha** de proteção
- **Ilimitado** em viewers

## 🎯 Checklist Final

Antes de compartilhar o link:

- [ ] Dashboard carrega corretamente
- [ ] Todos os gráficos aparecem
- [ ] Filtros funcionam
- [ ] Temas (claro/escuro) funcionam
- [ ] Tooltips aparecem corretamente
- [ ] Performance está aceitável

## 🆘 Problemas Comuns

### Erro de Memória
- Reduza o tamanho dos dados
- Use `.parquet` em vez de `.csv`
- Otimize ainda mais as colunas

### App muito lento
- Verifique se `@st.cache_data` está aplicado
- Considere reduzir período de dados
- Otimize queries do pandas

### Erro ao fazer push
- Arquivo muito grande → Use Git LFS
- Credenciais inválidas → Configure `git config`

## 📞 Suporte

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** Para problemas do código

---

Boa sorte com o deploy! 🚀
