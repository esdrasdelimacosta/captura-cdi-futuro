import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text 

#variaveis conexao banco
server = '10.175.84.61'
database = 'Solis'
username = 'integr_db'
password = '6FJtQ4g$L5VW'

# Função para criar conexão com o SQLAlchemy
def conecta_banco_alchemy():
    '''
    Cria um engine SQLAlchemy para o banco de dados SQL Server.
    '''
    connection_string = (
        f'mssql+pyodbc://{username}:{password}@{server}/{database}?'
        'driver=ODBC+Driver+17+for+SQL+Server'
    )
    engine = create_engine(connection_string)
    
    return engine

def conecta_banco():

    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)

def insert_data_to_table(df, table_name):
    """
    Insere dados do DataFrame na tabela especificada no SQL Server.
    """
    try:
        # Conecta ao banco de dados
        conn = conecta_banco()
        cursor = conn.cursor()

        # Prepara o comando SQL para inserção
        placeholders = ', '.join(['?'] * len(df.columns))
        columns = ', '.join(df.columns)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Itera sobre as linhas do DataFrame e insere os dados
        for row in df.itertuples(index=False, name=None):
            cursor.execute(sql, row)

        # Salva as alterações no banco de dados
        conn.commit()
        print(f"Dados inseridos com sucesso na tabela {table_name}.")

    except Exception as e:
        print(f"Erro ao inserir os dados na tabela {table_name}: {e}")

    finally:
        # Fecha a conexão
        conn.close()