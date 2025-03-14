import requests
from bs4 import BeautifulSoup
import os


def get_text_from_page(url):
    """Extrai o texto principal de uma página da wiki."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar {url}")
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='mw-parser-output')

    if content:
        text = '\n'.join(p.get_text() for p in content.find_all(['p', 'h1', 'h2', 'h3', 'h4']))
        return text

    return ""


def get_sublinks(base_url):
    """Coleta links internos relevantes para extração."""
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Erro ao acessar {base_url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    base_domain = "https://tormenta-collab.fandom.com"

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/pt-br/wiki/') and ':' not in href:
            links.add(base_domain + href)

    return list(links)


def save_to_txt(filename, text):
    """Salva o conteúdo extraído em um arquivo TXT no diretório correto."""
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "infobook")
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Texto salvo em '{filepath}'")


def main():
    base_url = "https://tormenta-collab.fandom.com/pt-br/wiki/Tormenta_20_Collab"
    links = get_sublinks(base_url)

    all_text = ""
    for link in [base_url] + links:
        print(f"Extraindo {link}...")
        all_text += get_text_from_page(link) + "\n\n"

    save_to_txt("tormenta_20_collab.txt", all_text)
    print("Extração concluída!")


if __name__ == "__main__":
    main()
