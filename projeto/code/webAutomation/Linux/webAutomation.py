import sys
import os
from pathlib import Path

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
import time

class WebAutomation:
    def __init__(self, code_input=None, driver_path=None):
        self.code_input = code_input
        
        if driver_path is None:
            driver_path = os.path.join(os.path.dirname(__file__), "chromedriver")
        
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver não encontrado em: {driver_path}")
        
        os.chmod(driver_path, 0o755)
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def open_site(self, url):
        print(f"A Abrir {url}")
        self.driver.get(url)
        time.sleep(0.5)
    
    def submit_code(self, code_output):
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
            
            code_input.value = '';
            
            code_input.value = arguments[0];
            
        
            code_input.dispatchEvent(new Event('input', { bubbles: true }));
            code_input.dispatchEvent(new Event('change', { bubbles: true }));
            
    
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

    # def close(self):
    #     """Fecha o navegador"""
    #     self.driver.quit()




# main()


