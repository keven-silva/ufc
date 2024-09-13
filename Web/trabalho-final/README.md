# Documentação: Como Iniciar o Projeto

Para iniciar o projeto, siga os passos abaixo:

1. Crie um ambiente virtual (venv) para isolar as dependências do projeto. Você pode usar o seguinte comando:

    ```
    python -m venv nome_do_ambiente
    ```

2. Ative o ambiente virtual. Dependendo do sistema operacional, o comando pode variar:

    - No Windows:
      ```
      nome_do_ambiente\Scripts\activate
      ```

    - No macOS/Linux:
      ```
      source nome_do_ambiente/bin/activate
      ```

3. Caso o python seja na versão 12 ou maior instale o **Poetry**, que é uma ferramenta de gerenciamento de dependências. Você pode instalá-lo usando o seguinte comando:

    ```
    pip install poetry
    ```
4. Caso o python seja uma versão menor que 12 instale usando o **pip**
    ```
    pip install -r requirements.txt
    ```
5. Navegue até o diretório raiz do projeto e execute o seguinte comando para instalar as dependências:

    ```
    poetry install
    ```

6. Copie as variaveis do arquivo **.env.example** para um novo arquivo **.env**

7. Após a instalação das dependências, você pode iniciar o projeto executando o seguinte comando:

    ```
    python -m src
    ```

Pronto! Agora você está pronto para começar a trabalhar no projeto. Certifique-se de que o ambiente virtual esteja sempre ativado ao trabalhar no projeto.
