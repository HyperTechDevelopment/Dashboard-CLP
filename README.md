
# Dashboard CLP - Controle de Lavagem de Placas

## Descrição

Este projeto é um complemento ao sistema CLP - Controle de Lavagem de Placas. Ele exibe um gráfico mostrando a quantidade de seriais que cada linha no ambiente industrial está recebendo, com a possibilidade de aplicar filtros por turno e modelo.

## Instalação

1. Clone o repositório:
    ```bash
    git clone <URL-do-repositório>
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd <nome-do-diretório>
    ```

3. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute o aplicativo Flask:
    ```bash
    flask run
    ```

2. Acesse o aplicativo em seu navegador em `http://127.0.0.1:5000`.

## Configuração

O aplicativo requer uma conexão com o banco de dados SQLite localizado no caminho especificado. Certifique-se de que o caminho do banco de dados esteja correto e acessível:

```python
conn = sqlite3.connect(r"INSIRA O CAMINHO DO BANCO AQUI.")
```
Atente-se para o nome do banco, para que não haja erros: BDCALL.db

## Observação

Se optar por hospedar esta dashboard em um servidor, lembre-se de que o processo de comunicação será diferente, pois foi utilizado o SQLite.

Se utilizar Linux para hospedar por exemplo, crie um script que envie o arquivo .db a cada X minutos para o servidor, e modifique o caminho do banco para que extraia os dados.
