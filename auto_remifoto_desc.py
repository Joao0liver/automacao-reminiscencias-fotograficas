from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import time
import json

URL = 'https://sistemasgerenciais.com.br/camaraitajuba/memorial/'

TOTAL_IMAGENS = 5

with sync_playwright() as p:

    # Abre o navegador e o executa mostrando a janela (headless=False)
    navegador = p.chromium.launch(headless=False)
    # Cria uma nova página
    pagina = navegador.new_page()

    pagina.goto(URL)

    pasta = Path('desc')
    pasta.mkdir(exist_ok=True)

    descricoes = []

    for numero in range(1, TOTAL_IMAGENS + 1):

        seletor = f'#id_sc_field_descricao_{numero}'

        print(f'\nProcurando descrição da imagem {numero}/{TOTAL_IMAGENS}...')

        while pagina.locator(seletor).count() == 0:
            pagina.mouse.wheel(0, 1500)
            time.sleep(0.5)

        texto = pagina.locator(f'{seletor} font').inner_text()

        if not texto:
            print(f'Imagem {numero}: descrição não encontrada.')
            continue

        print(f'Descrição: {texto}')

        if texto in descricoes:
            print('Descrição já armazenada.')
            continue

        descricoes.append({
            'foto': texto,
            'descricao': texto
        })

    with open('descricoes.json', 'w', encoding='utf-8') as arquivo:
        json.dump(descricoes, arquivo, ensure_ascii=False, indent=4)

    navegador.close()
