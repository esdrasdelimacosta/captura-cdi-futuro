import os
import time
from utils.captura_dados import captura_dados_b3
from utils.db_integracao import insert_data_to_table

def main():
    os.system('cls')
    tempo_inicial = time.time()
    
    print("[INFO] Iniciando Captura de dados...")
    df = captura_dados_b3()
    if df is not None:
        print("[INFO] Iniciando a importação dos dados para o SQL Server...")
        insert_data_to_table(df,'Solis.Indice.CDI_Futuro')
    else:
        print('Não existem dados a serem inseridos!')
    tempo_final = time.time()
    print('******************************************************')
    print(f"[INFO] Tempo total de execução: {tempo_final - tempo_inicial:.4f} segundos")
 
if __name__ == '__main__':
    main()