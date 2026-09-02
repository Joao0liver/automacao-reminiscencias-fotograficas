from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import time
import json

URL = 'https://sistemasgerenciais.com.br/camaraitajuba/memorial/'

TOTAL_IMAGENS = 532

with sync_playwright() as p:

    # Abre o navegador e o executa mostrando a janela (headless=False)
    navegador = p.chromium.launch(headless=False)
    # Cria uma nova página
    pagina = navegador.new_page()

    # Acessa a URL
    pagina.goto(URL)

    # Cria o caminho para as pastas e as cria caso não existam
    pasta_fotos = Path('fotos')
    pasta_desc = Path('desc')
    pasta_fotos.mkdir(exist_ok=True)
    pasta_desc.mkdir(exist_ok=True)

    # Cria as listas/coleções para controle
    imagens_baixadas = set()
    descricoes = []

    # Percorre o total de fotos existentes no site
    for numero in range(1, TOTAL_IMAGENS + 1):

        # Registra os ids das fotos e descrições (blocos <span> e <a> no HTML, respectivamente) / Monta os seletores
        seletor_fotos = f'#id_sc_field_sugestao_{numero}'
        seletor_desc = f'#id_sc_field_descricao_{numero}'

        print(f'\nProcurando imagem {numero}/{TOTAL_IMAGENS}...')

        # Enquanto o id da foto X não for encontrado, scrolla o site para baixo (pois o site não carrega todas as fotos de uma vez)
        while pagina.locator(seletor_fotos).count() == 0:
            pagina.mouse.wheel(0, 1500)
            time.sleep(0.5)

        # Pega o link da foto através do seletor (que está em um bloco de link <a>)
        link = pagina.locator(f'{seletor_fotos} a')
        href = link.get_attribute('href')

        # Se não houver um href, não existe link e o código vai para a próxima iteração (continue)
        if not href:
            print(f'Imagem {numero}: link não encontrado.')
            continue

        # Verifica se existe um bloco <font> para descrição, do contrário, o texto vai vazio no .json
        if pagina.locator(f'{seletor_desc} font').count() > 0:
            texto = pagina.locator(f'{seletor_desc} font').inner_text()
        else:
            texto = ''

        # Monta a URL completa
        url_imagem = urljoin(pagina.url, href)
        print(f'URL: {url_imagem}')

        # Se a URL da foto existe na coleção de controle, não adiciona e vai pra próxima iteração (continue)
        if url_imagem in imagens_baixadas:
            print('Imagem já baixada.')
            continue

        # Baixa a imagem de forma direta pela URL
        resposta = pagina.request.get(url_imagem)

        # Se a resposta HTTP foi bem-sucedida (se baixou a foto)
        if resposta.ok:
            # Pega o nome do arquivo baixado
            nome_arquivo = Path(url_imagem).name

            # Monta o caminho para a pasta de fotos (fotos/nomefoto.jpg)
            arquivo = pasta_fotos / nome_arquivo

            # Cria o arquivo com modo de escrita binária (write binary = wb), pois imagens são arquivos binários
            with open(arquivo, 'wb') as f:
                # Pega o conteúdo recebido (resposta.body()) e grava no arquivo criado (f)
                f.write(resposta.body())

            # Registra na coleção que a URL foi baixada
            imagens_baixadas.add(url_imagem)
            print(f'✓ Salva em: {arquivo}')

            # Registra na lista o nome da foto e a descrição associada a ela
            descricoes.append({
                'foto': nome_arquivo,
                'descricao': texto
            })
        else:
            # Caso a resposta HTTP seja mal-sucedida (se não baixou a foto)
            print(f'ERRO ao baixar imagem {numero}: HTTP {resposta.status}')

    # Cria o arquivo .json em modo de escrita (write = w) com encoding dos caracteres do português
    with open(f'{pasta_desc}/descricoes.json', 'w', encoding='utf-8') as arquivo:
        # Converte a lista em JSON, mantendo os caracteres especiais (ensure_ascii=False) - indent=4 organiza o JSON, não deixando todos os registros em uma única linha
        json.dump(descricoes, arquivo, ensure_ascii=False, indent=4)

    navegador.close()