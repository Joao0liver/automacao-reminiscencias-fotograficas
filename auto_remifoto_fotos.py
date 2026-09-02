from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import time

URL = 'https://sistemasgerenciais.com.br/camaraitajuba/memorial/'

TOTAL_IMAGENS = 532

with sync_playwright() as p:

    # Abre o navegador e o executa mostrando a janela (headless=False)
    navegador = p.chromium.launch(headless=False)
    # Cria uma nova página
    pagina = navegador.new_page()

    pagina.goto(URL)

    pasta = Path('fotos')
    pasta.mkdir(exist_ok=True)

    imagens_baixadas = set()

    for numero in range(1, TOTAL_IMAGENS + 1):

        seletor = f'#id_sc_field_sugestao_{numero}'

        print(f'\nProcurando imagem {numero}/{TOTAL_IMAGENS}...')

        while pagina.locator(seletor).count() == 0:
            pagina.mouse.wheel(0, 1500)
            time.sleep(0.5)

        link = pagina.locator(f'{seletor} a')

        href = link.get_attribute('href')

        if not href:
            print(f'Imagem {numero}: link não encontrado.')
            continue

        url_imagem = urljoin(pagina.url, href)
        print(f'URL: {url_imagem}')

        if url_imagem in imagens_baixadas:
            print('Imagem já baixada.')
            continue

        resposta = pagina.request.get(url_imagem)

        if resposta.ok:
            nome_arquivo = Path(url_imagem).name

            arquivo = pasta / nome_arquivo

            with open(arquivo, 'wb') as f:
                f.write(resposta.body())

            imagens_baixadas.add(url_imagem)

            print(f'✓ Salva em: {arquivo}')

        else:
            print(f'ERRO ao baixar imagem {numero}: HTTP {resposta.status}')

    navegador.close()
