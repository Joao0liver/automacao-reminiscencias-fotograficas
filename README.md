# 📸 Automação — Reminiscências Fotográficas

Automação desenvolvida para auxiliar na coleta e organização dos conteúdos do projeto **Reminiscências Fotográficas**, da Câmara Municipal de Itajubá/MG.

O projeto utiliza **Python e Playwright** para acessar a página do projeto, localizar as fotografias carregadas dinamicamente, realizar o download das imagens e registrar as descrições associadas a cada fotografia em um arquivo JSON - associando nome da foto e descrição.

Há três arquivos no projeto, um que apenas faz o downlaod das fotos, outro que pega apenas as descrições e um que faz tudo junto.

## 🎯 Objetivo da Automação

O objetivo destes scripts é facilitar o processo de recuperação e armazenamento das fotografias e imagens disponibilizadas na página do projeto **Reminiscências Fotográficas**, da Câmara Municipal de Itajubá/MG.

A automação foi desenvolvida com o propósito de agilizar a coleta desses conteúdos, que posteriormente serão migrados para o novo site da Câmara Municipal, cujo desenvolvimento conta com minha participação ativa. O projeto está sendo desenvolvido no contexto das minhas atividades de estágio, nas quais atuo como **Analista de TI e Desenvolvedor** da própria Câmara - datados do momento de escrita dessa documentação.

## 🛠️ Tecnologias e bibliotecas utilizadas

### 🐍 Python

Linguagem utilizada para desenvolver toda a automação.

O projeto utiliza recursos da biblioteca padrão do Python, como:

- `pathlib` — manipulação de caminhos e diretórios;
- `urllib.parse` — construção e manipulação de URLs;
- `time` — controle de intervalos durante a navegação;
- `json` — criação e armazenamento dos dados coletados em formato JSON.

### 🎭 Playwright

Biblioteca utilizada para automação de navegadores.

Neste projeto, o Playwright é responsável por:

- 🌐 abrir o navegador Chromium;
- 🔗 acessar a página do projeto;
- 🔎 localizar elementos HTML;
- 🖱️ realizar a rolagem da página;
- 📷 obter os links das fotografias;
- 📥 realizar o download das imagens.

A utilização do Playwright é especialmente importante porque as fotografias são carregadas dinamicamente conforme a página é percorrida.

### 📁 pathlib

Biblioteca nativa do Python utilizada para trabalhar com arquivos e diretórios de maneira independente do sistema operacional.

É utilizada, por exemplo, para criar as pastas `fotos` e `desc` e definir os caminhos dos arquivos baixados.

### 📋 json

Biblioteca nativa do Python utilizada para armazenar as descrições coletadas em arquivos JSON.

O arquivo gerado permite manter uma relação entre o nome da fotografia e sua respectiva descrição.

---

## 📂 Estrutura do projeto

```text
automacao-reminiscencias-fotograficas/
│
├── auto_remifoto.py
├── auto_remifoto_desc.py
├── auto_remifoto_fotos.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── fotos/
│   └── imagens baixadas
│
└── desc/
    └── descricoes.json
```

### 📜 Scripts

#### ⚙️ `auto_remifoto.py`

Executa o fluxo completo da automação.

O script:

1. 🌐 acessa a página do projeto;
2. 📷 percorre as fotografias disponíveis;
3. 🔗 localiza o link de cada imagem;
4. 📥 baixa as imagens;
5. 📝 coleta as descrições;
6. 💾 gera o arquivo `desc/descricoes.json`.

#### 📸 `auto_remifoto_fotos.py`

Responsável exclusivamente pelo **download das fotografias**.

As imagens são armazenadas na pasta:

```text
fotos/
```

#### 📝 `auto_remifoto_desc.py`

Responsável pela **coleta das descrições** das fotografias.

As informações são armazenadas em formato JSON.

---

# 💻 Como executar o projeto

## 📋 1. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- 🐍 Python 3;
- 🔧 Git;
- 💻 um terminal (PowerShell, CMD, Bash etc.).

Recomenda-se utilizar uma versão recente do Python.

Para verificar a instalação:

```bash
python --version
```

E:

```bash
git --version
```

---

## 📥 2. Clonar o repositório

Clone o projeto utilizando Git:

```bash
git clone https://github.com/Joao0liver/automacao-reminiscencias-fotograficas.git
```

Entre na pasta do projeto:

```bash
cd automacao-reminiscencias-fotograficas
```

---

## 🌱 3. Criar um ambiente virtual

É recomendado utilizar um ambiente virtual para evitar conflitos entre as dependências do projeto e as bibliotecas instaladas globalmente.

### 🪟 Windows

```powershell
python -m venv venv
```

Ative o ambiente virtual:

```powershell
venv\Scripts\activate
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

```text
(venv) C:\caminho\do\projeto>
```

### 🐧 Linux/macOS

```bash
python3 -m venv venv
```

Ative o ambiente:

```bash
source venv/bin/activate
```

---

## 📦 4. Instalar as dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

As principais dependências do projeto estão relacionadas ao **Playwright** e seus componentes de execução.

---

## 🌐 5. Instalar o navegador do Playwright

Após instalar as dependências, instale o navegador Chromium utilizado pela automação:

```bash
playwright install chromium
```

> ⚠️ **Importante:** esse passo é necessário para que o Playwright consiga iniciar o navegador utilizado pelos scripts.

---

# ▶️ Executando a automação

Depois de configurar o ambiente, existem três formas principais de executar o projeto.

## 🚀 Automação completa

Para executar o processo completo:

```bash
python auto_remifoto.py
```

Esse script cria automaticamente as pastas necessárias:

```text
fotos/
desc/
```

As fotografias são salvas em `fotos/` e as descrições são registradas em:

```text
desc/descricoes.json
```

O script atualmente está configurado para percorrer todas as **532 fotografias** dispostas na página.

---

# 🔄 Funcionamento

A automação acessa a página do projeto e utiliza seletores HTML para localizar cada fotografia e sua descrição.

Como os conteúdos são carregados dinamicamente, o script realiza rolagens sucessivas na página até que o elemento correspondente à fotografia seja encontrado.

De maneira simplificada, o fluxo é:

```text
              🌐 Página do projeto
                       │
                       ▼
              🎭 Abertura do Chromium
                       │
                       ▼
               🖱️ Navegação pela página
                       │
                       ▼
              🔎 Localização da fotografia
                       │
               ┌───────┴───────┐
               ▼               ▼
         📥 Download       📝 Descrição
               │               │
               ▼               ▼
            📁 fotos/       📁 desc/
                               │
                               ▼
                       📄 descricoes.json
```

---

# ⚠️ Observações

- 🌐 O navegador Chromium será aberto durante a execução, pois os scripts utilizam `headless=False`.
- ⏱️ A velocidade da execução depende da quantidade de imagens e da conexão com a internet.
- 💾 Os arquivos baixados são armazenados localmente.
- 🔧 O projeto depende da estrutura HTML da página de origem. Alterações nos elementos ou identificadores utilizados pelo site podem exigir alterações nos seletores dos scripts.
- 📜 A execução deve respeitar os termos de uso e as condições de acesso do site de origem.

---

# 👨‍💻 Autor

Desenvolvido por **João Augusto de Oliveira**.
