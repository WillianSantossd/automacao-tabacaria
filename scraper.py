from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def buscar_produto(produto_busca):
    driver = iniciar_driver()
    wait = WebDriverWait(driver, 20)
    resultados = []

    try:
        driver.get("https://www.oasistabacaria.com/")
        
        # Confirmar idade
        try:
            botao_18 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'sim', 'SIM'), 'SIM')]")))
            driver.execute_script("arguments[0].click();", botao_18)
        except: pass

        # Buscar produto
        caixa_busca = wait.until(EC.element_to_be_clickable((By.NAME, "q")))
        caixa_busca.send_keys(produto_busca)
        caixa_busca.send_keys(Keys.RETURN)

        # Ajustar para o máximo de itens por página
        try:
            seletor_elemento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#limiter")))
            dropdown = Select(seletor_elemento)
            dropdown.select_by_index(len(dropdown.options) - 1)
            time.sleep(3)
        except: pass

        while True:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.item.product.product-item")))
            time.sleep(2)
            produtos = driver.find_elements(By.CSS_SELECTOR, "li.item.product.product-item")

            for produto in produtos:
                nome = produto.find_element(By.CSS_SELECTOR, ".product-item-link").text
                preco = produto.find_element(By.CSS_SELECTOR, ".price-wrapper .price").text
                link = produto.find_element(By.CSS_SELECTOR, ".product-item-link").get_attribute("href")
                
                # Verificar Disponibilidade
                # Se encontrar o botão de adicionar ao carrinho, está disponível
                try:
                    produto.find_element(By.CSS_SELECTOR, "button.tocart")
                    estoque = "Disponível"
                except:
                    estoque = "Esgotado"

                # Lógica simples de Marca (Busca palavras conhecidas no nome)
                marcas_conhecidas = ["RAW", "OCB", "SQUADAFUM", "ZOMO", "PAPELITO", "ELEMENTS", "BEM BOLADO"]
                marca_encontrada = "Outras"
                for m in marcas_conhecidas:
                    if m in nome.upper():
                        marca_encontrada = m
                        break

                resultados.append({
                    "PRODUTO": nome,
                    "MARCA": marca_encontrada,
                    "VALOR": preco,
                    "DISPONIBILIDADE": estoque,
                    "LINK": link,
                    "DATA": time.strftime("%d/%m/%Y")
                })

            # Próxima página
            try:
                botao_proximo = driver.find_element(By.CSS_SELECTOR, "a.action.next")
                driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
                time.sleep(1)
                botao_proximo.click()
            except:
                break 

        return resultados
    finally:
        driver.quit()