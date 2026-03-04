import os
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

# Configurações
SEARCH_QUERY = "machine+learning" # Você pode mudar o tema aqui
MAX_DOCUMENTS = 50               # Comece com 50 para testar
DATA_FOLDER = Path("titan/data/raw_pdfs")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

def download_arxiv_pdfs():
    print(f"Iniciando busca por '{SEARCH_QUERY}' no arXiv...")
    url = f"https://arxiv.org/search/?query={SEARCH_QUERY}&searchtype=all&source=header"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontra os links que levam ao PDF
    pdf_links = []
    for link in soup.find_all('a', href=True):
        if '/pdf/' in link['href']:
            full_url = link['href']
            if not full_url.startswith('http'):
                full_url = 'https://arxiv.org' + full_url
            pdf_links.append(full_url)
    
    count = 0
    for link in pdf_links[:MAX_DOCUMENTS]:
        try:
            filename = f"paper_{count}.pdf"
            filepath = DATA_FOLDER / filename
            
            print(f"Baixando {filename}...")
            pdf_data = requests.get(link).content
            
            with open(filepath, 'wb') as f:
                f.write(pdf_data)
            
            count += 1
            time.sleep(1) # Respeita o servidor para não ser bloqueado
            
        except Exception as e:
            print(f"Erro ao baixar {link}: {e}")

    print(f"Download concluído! {count} PDFs salvos em {DATA_FOLDER}")

if __name__ == "__main__":
    download_arxiv_pdfs()