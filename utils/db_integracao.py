import pyodbc
import pandas as pd
from airflow.hooks.base import BaseHook

def conecta_banco():
    driver = "ODBC Driver 17 for SQL Server"
    conn = BaseHook.get_connection("sqlserver_conn_solis")  # Nome da conexão no Airflow
    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={conn.host};"
        f"DATABASE={conn.schema};"
        f"UID={conn.login};"
        f"PWD={conn.password};"
        f"PORT={conn.port or 1433}"
    )

    connection = pyodbc.connect(conn_str)
    return connection

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