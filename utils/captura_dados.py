from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import time
import pandas as pd
from datetime import timedelta, date
from fixeds.constants import TEMP_DIR

def captura_dados_b3():
   # URL da página
   url = 'https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-taxas-referenciais-bmf-ptBR.asp'


   # Cria uma pasta temporária
   temp_profile = tempfile.mkdtemp()

   # Configurações do Chrome para definir o diretório de download e modo headless
   chrome_options = Options()
   chrome_options.add_argument('--headless=new')  # Utiliza o novo modo headless
   chrome_options.add_argument(f"--user-data-dir={temp_profile}")
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')
   chrome_options.add_argument('--remote-debugging-port=0')  # <-- Adicione esta linha aqui!
   chrome_options.add_experimental_option('prefs', {
      'download.default_directory': TEMP_DIR,
      'download.prompt_for_download': False,
      'download.directory_upgrade': True,
      'safebrowsing.enabled': True
   })

   # Inicializa o WebDriver
   driver = webdriver.Chrome(service=Service(), options=chrome_options)

   try:
      # Acessa a página
      driver.get(url)

      # Aguarda até que o link de download esteja presente
      wait = WebDriverWait(driver, 10)
      download_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Download')))

      # Clica no link de download
      download_link.click()

      # Aguarda o download ser concluído
      time.sleep(5)  # Ajuste o tempo conforme necessário

      # Verifica se o arquivo foi baixado
      files = os.listdir(TEMP_DIR)
      xls_files = [f for f in files if f.endswith('.xls')]
      if xls_files:
         tabelas = pd.read_html(TEMP_DIR + '/' + xls_files[0], decimal=',', thousands='.')
         df = tabelas[0]

         # Definindo a data atual
         data_atual = date.today()

         # Atribuindo novos nomes às colunas
         df.columns = ['Dias_Corridos', 'Taxa_252', 'Taxa_360']
         
         # Removendo as linhas onde 'Dias_Corridos' é NaN
         df = df.dropna(subset=['Dias_Corridos'])
         
         df['Data_Referencia'] = data_atual
         df['Data_Posicao'] = df['Dias_Corridos'].apply(lambda x: data_atual + timedelta(days=x))
         
         print("Dataframe carregado com sucesso.")
         return df[['Data_Referencia', 'Data_Posicao', 'Taxa_252', 'Taxa_360']]

      else:
         print('O download não foi concluído ou o arquivo não foi encontrado.')
         return None         

   finally:
      # Encerra o WebDriver
      driver.quit()