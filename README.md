# Pipeline de ETL simplificado envolvendo dois bancos de dados

Neste projeto, foram criados dois bancos de dados, Fonte e Alvo, escritos em **postgresql** e acessados através de uma API escrita em **fastapi**. Adicionalmente, foi feito um script em python que busca dados do banco Fonte e escreve os resultados no banco de dados Alvo.

## Preparando o ambiente

Primeiramente, para evitar conflitos entre versões de bibliotecas utilizadas no projeto, recomenda-se a criação de uma 'VENV' (virtual environment).

**_python3 -m venv venv_**

Para acessar o ambiente virtual, execute:

**_source venv/bin/activate_**

Em seguida, vamos instalar as dependências nesse ambiente virtual:

**_pip install fastapi_**

**_pip install uvicorn_**

**_pip install sqlalchemy_**

**_pip install psycopg2-binary_**

**_pip install pandas_**

**_pip install httpx_**

Após isso, podemos executar o projeto. Certifique-se de ter o Docker instalado em sua máquina. Para subir o banco de dados, execute:

**_make psql-up_**

Alternativamente, os comandos **_make psql-down_** e **_make psql-restart_** desativam e reiniciam um novo banco de dados.

Finalmente, para iniciar o projeto, execute:

**_make start-dev_**

# Estrutura do projeto

## Banco de Dados Fonte

- `data`
  - id
  - timestamp
  - wind_speed
  - power
  - ambient_temprature

## Banco de Dados Alvo

- `signal`
  - id
  - name

- `data`
  - id
  - timestamp
  - signal_id
  - value

## Acessando e utilizando as funções do projeto

O projeto abrirá na url [http://127.0.0.1:8000](http://127.0.0.1:8000). Para ver a lista de métodos implementados, pode-se acessar em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### /all_data/ 

Retorna todos os dados da tabela `data` do Banco de Dados Fonte. Neste caso, os dados inseridos foram aleatórios com frequência 1-minutal e intervalo de 10 dias, iniciando no dia **27 de Maio de 2024**

### /data_in_time_range/

Retorna todos os dados contidos num intervalo de tempo definidos por duas datas no formato datetime. Pode-se inserir esses valores na [Swagger UI](http://127.0.0.1:8000/docs#/default/read_data_range_data_in_time_range__get) ou como uma query search. Por exemplo: http://127.0.0.1:8000/data_in_time_range/?start_time=2024-05-27T00:00:00&end_time=2024-05-27T00:05:00

### /data_in_day/

Retorna todos os dados coletados no dia, definido por uma data no formato date. A busca do script ETL é feita por essa requisição. Exemplo: http://127.0.0.1:8000/data_in_day/?day=2024-05-27

### /signals/

Retorna todos os dados da tabela `signal` do Banco de Dados Alvo

### /alvo/data/

Retorna todos os dados da tabela `data` do Banco de Dados Alvo

# ETL

Dentro da pasta do projeto, execute o script _etl.py:_

**_python3 app/etl.py_**

O programa irá pedir para continuar com mais uma busca de dados e, se prosseguir, irá pedir uma data. Ao fornecer uma data de um dia válido no formato requerido, o programa grava os dados na tabela `data` do Banco de Dados Alvo. Para verificar os dados carregados, pode-se ver na [Swagger UI](http://127.0.0.1:8000/docs#/default/read_alvo_data_alvo_data_get) ou pela url [http://127.0.0.1:8000/all_data/](http://127.0.0.1:8000/all_data/)
