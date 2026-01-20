from parserPascal import *
from lexer_pascal import *
from analiseSemantica import *
from random import *
from codigoMaquina import *
from inputs import *
import time
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "webAutomation" / "Linux"))
from webAutomation import WebAutomation


def main(input_code):

    # chamar o parser
    parsed = parser.parse(input_code)

    # dicionario global
    dic_global = dict()
    dic_global = criaDicMainVars(parsed, dic_global)

    # gerar codigo para as funcoes
    codigo_funs, dic_global = geraFuns(getFuns(parsed), dic_global)  
    dic_local = dict()
    
    # gerar a main
    result = "\nSTART:\n" + computaFuncao(parsed, dic_local, dic_global) + "STOP\n\n" + codigo_funs 

    # web automation
    automation = WebAutomation(result)
    automation.open_site("https://ewvm.epl.di.uminho.pt/")
    automation.submit_code(automation.code_input)
    print("Browser aberto. CTRL+C para fechar")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("A Fechar o browser")
        automation.driver.quit()


main(input_fac)  

