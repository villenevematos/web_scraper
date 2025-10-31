from bs4 import BeautifulSoup
import requests

def fetch_top_titles(url, limit=10, timeout=10):
    """Busca até `limit` títulos das manchetes da página principal do G1.

    Retorna uma lista de strings (pode ser menor que `limit` se não houver elementos suficientes).
    Define o cabeçalho da requisição para simular um navegador real

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36'
    }

    try:
        # Faz a requisição HTTP para a URL fornecida
        resp = requests.get(url, headers=headers, timeout=timeout)
        # Lança exceção se o status da resposta indicar erro
        resp.raise_for_status()
    except requests.RequestException as e:
        # Em caso de erro na requisição, imprime a mensagem e retorna lista vazia
        print(f"Erro na requisição: {e}")
        return []

    # Cria o objeto BeautifulSoup para analisar o conteúdo HTML
    soup = BeautifulSoup(resp.content, 'html.parser')

    # Encontrar todos os links de manchete com a classe usada no site
    links = soup.find_all('a', class_='feed-post-link')
    # Inicializa listas para armazenar títulos e links, e um conjunto para evitar duplicatas
    titles = []
    lista_links = []
    seen = set()
    
    # Itera sobre os elementos encontrados
    for a in links:
        print(a)
        # Ignora elementos nulos
        if a is None:
            continue # Ignora se o texto estiver vazio

        # Extrai o texto do link, removendo espaços
        text = a.get_text(strip=True)
        if not text:
            continue
        if text in seen:
            continue 
        # Adiciona o título ao conjunto de vistos
        seen.add(text) 
        # Adiciona o título à lista de títulos
        titles.append(text) 
        # Adiciona o link à lista de links
        lista_links.append(a.get('href'))
        if len(titles) >= limit:
            break

    return titles


url = "https://g1.globo.com/"

if __name__ == '__main__':
    # Exemplo: imprimir até 10 títulos
    titulos = fetch_top_titles(url, limit=10)
    if not titulos:
        print('Nenhum título encontrado.')
    else:
        for idx, t in enumerate(titulos, start=1):
            print(f"{idx:2d}. {t}", '-' * 40, sep='\n')
    