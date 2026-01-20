import sys
import os
from pathlib import Path
import platform

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from codigoMaquina import *
from parserPascal import *
from analiseSemantica import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class WebAutomationMacos:
    def __init__(self, code_input=None):
        """
        Inicializar o WebAutomation para macOS com ChromeDriver.
        :param code_input: Código a submeter (opcional).
        """
        if platform.system() != "Darwin":
            raise OSError("Esta classe é apenas para macOS")
        
        self.code_input = code_input
        
        # Configurar opções do Chrome para macOS
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Usar webdriver-manager para gerenciar ChromeDriver automaticamente
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✓ ChromeDriver inicializado com sucesso no macOS")
        except Exception as e:
            print(f"✗ Erro ao inicializar ChromeDriver: {e}")
            raise
    
    def open_site(self, url):
        """Abre o site do EWVM"""
        print(f"A Abrir {url}")
        self.driver.get(url)
        time.sleep(0.5)
    
    def submit_code(self, code_output):
        """Submete o output do programa no site EWVM"""
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "form"))
        )
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "code"))
        )
        time.sleep(0.5)
        
        result = self.driver.execute_script("""
            const code_input = document.getElementById('code');
            const form = document.getElementById('form');
            
            if (!code_input || !form) {
                return "missing form or code input";
            }
            
            // Garantir que o input está vazio ANTES de preencher
            code_input.value = '';
            
            // Agora preencher o código
            code_input.value = arguments[0];
            
            // Disparar eventos de mudança
            code_input.dispatchEvent(new Event('input', { bubbles: true }));
            code_input.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Verificar se foi preenchido corretamente
            const lines = code_input.value.split('\\n');
            return {
                total_chars: code_input.value.length,
                total_lines: lines.length,
                firstLines: lines.slice(0, 10).join('\\n')
            };
        """, code_output)
        
        time.sleep(0.5)
        
        self.driver.execute_script("""
            document.getElementById('form').submit();
        """)
        
        time.sleep(1)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'button') and contains(text(), '>>')]"))
        )
        
        output_btn = self.driver.find_element(By.XPATH, "//div[contains(@class, 'button') and contains(text(), '>>')]")
        output_btn.click()
        time.sleep(0.5)
    
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser fechado")



if __name__ == "__main__":
    parsed = parser.parse(input_fac)

    dic_global = dict()

    dic_global = criaDicMainVars(parsed, dic_global)
    codigo_funs, dic_global = geraFuns(getFuns(parsed), dic_global)  # Captura ambos

    dic_local = dict()

    result = "\nSTART:\n" + computaFuncao(parsed, dic_local, dic_global) + "STOP\n\n" + codigo_funs 
    print(result)
    print("-----------\n", result)
    
    automation = WebAutomationMacos(result)
    automation.open_site("https://ewvm.epl.di.uminho.pt/")
    automation.submit_code(automation.code_input)
    print("Browser aberto. Pressione CTRL+C para fechar")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("A Fechar o browser")
        automation.driver.quit()