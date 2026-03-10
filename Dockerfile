# 1. Imagem base do Python 3.12 (leve)
FROM python:3.12-slim

# 2. Define a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia todo o seu código (mantendo a estrutura de pastas)
COPY . .

# 5. Expõe a porta que o Streamlit usa
EXPOSE 8501

# 6. Comando para rodar a aplicação
# Usamos flags para o Streamlit aceitar conexões externas
CMD ["streamlit", "run", "src/interface/app.py", "--server.port=8501", "--server.address=0.0.0.0"]