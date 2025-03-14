# discord-ai-bot-rpg

Um bot para auxiliar durante o RPG de mesa Tormenta 20 com informações de regras, itens, poderes, habilidades e tudo mais.

## O que é este projeto?

Este projeto é um bot para Discord desenvolvido em Python que auxilia jogadores de RPG de mesa, especificamente Tormenta 20. O bot oferece funcionalidades como rolagem de dados, reprodução de música, gerenciamento de fichas de personagens e geração de imagens usando IA.

## Funcionalidades

- **Rolagem de Dados**: Comando para rolar dados de diferentes tipos.
- **Música**: Comandos para tocar, pausar e parar músicas.
- **Gerenciamento de Fichas**: Comandos para criar, editar e visualizar fichas de personagens.
- **Geração de Imagens**: Comando para gerar imagens usando a API do HuggingFace.

## Como configurar o projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Conta no Discord e um servidor onde o bot será adicionado
- Token do bot do Discord
- Ollama instalado localmente
- Modelo mistral necessário baixado no Ollama

### Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/SeuUsuario/discord-ai-bot-rpg.git
    cd discord-ai-bot-rpg
    ```

2. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    ```env
    DISCORD_TOKEN=seu_token_do_discord
    OLLAMA_SERVER_URL=http://localhost:11434/api/generate
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Instale o Ollama localmente seguindo as instruções em [Ollama](https://ollama.com).

5. Baixe o modelo necessário no Ollama:
    ```sh
    ollama pull mistral
    ```

### Inicialização do Bot

Para iniciar o bot, execute o seguinte comando:
```sh
python main.py
```
### Testando o Bot

1. Adicione o bot ao seu servidor do Discord usando o link de autorização gerado no portal de desenvolvedores do Discord.
2. No servidor do Discord, use o comando `/ajuda` para listar todos os comandos disponíveis e suas funcionalidades.

## Estrutura do Projeto

- `config.py`: Arquivo de configuração que carrega as variáveis de ambiente.
- `main.py`: Arquivo principal que inicializa o bot e carrega as extensões.
- `commands/`: Diretório contendo os módulos de comandos do bot.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `README.md`: Este arquivo, com informações sobre o projeto.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

